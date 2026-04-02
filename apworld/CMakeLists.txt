include(APIgnore)
include(GitUtilities)

option(RRAP_BUILD_ARCHIPELAGO_PK3 "Create archipelago.pk3" ON)
option(RRAP_BUILD_APWORLD "Create ringracers.apworld" ON)

find_program(ZIP_EXECUTABLE zip)

#
# Generate the game's archipelago.pk3
# It's just our data folder packed into a zip
#

set(RRAP_ARCHIPELAGO_DATA_SOURCE_PATH "${CMAKE_SOURCE_DIR}/apworld/data")
set(RRAP_ARCHIPELAGO_GFX_SOURCE_PATH "${CMAKE_SOURCE_DIR}/apworld/graphics")

set(RRAP_ARCHIPELAGO_DATA_EXPORT_PATH "${CMAKE_BINARY_DIR}/bin/data")
set(RRAP_ARCHIPELAGO_DATA_EXPORT_FILE "${RRAP_ARCHIPELAGO_DATA_EXPORT_PATH}/archipelago.pk3")

set(RRAP_ARCHIPELAGO_DATA_STAGING_PATH "${CMAKE_BINARY_DIR}/apworld/pk3_staging")

if(RRAP_BUILD_ARCHIPELAGO_PK3)
	if(NOT ZIP_EXECUTABLE)
		message(WARNING "zip was not found; archipelago.pk3 cannot be created")
		add_custom_target(
			rrap_pk3 ALL
			COMMENT "zip was not found; archipelago.pk3 cannot be created"
		)
	else()
		file(GLOB_RECURSE PK3_SOURCES
			"${RRAP_ARCHIPELAGO_DATA_SOURCE_PATH}/*"
		)

		add_custom_command(
			COMMENT "Staging archipelago.pk3"
			DEPENDS ${PK3_SOURCES}
			WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
			OUTPUT "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/.prepped"

			COMMAND ${CMAKE_COMMAND} -E remove_directory "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}"
			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/archipelago"
			COMMAND ${CMAKE_COMMAND} -E copy_directory "${RRAP_ARCHIPELAGO_DATA_SOURCE_PATH}" "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/archipelago"
			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/graphics"
			COMMAND ${CMAKE_COMMAND} -E copy_directory "${RRAP_ARCHIPELAGO_GFX_SOURCE_PATH}" "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/graphics"
			COMMAND ${CMAKE_COMMAND} -E touch "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/.prepped"
		)

		add_custom_command(
			COMMENT "Packaging archipelago.pk3"
			DEPENDS "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/.prepped"
			WORKING_DIRECTORY "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}"
			OUTPUT "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}"

			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_ARCHIPELAGO_DATA_EXPORT_PATH}"
			COMMAND zip -r "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}" archipelago graphics
		)

		add_custom_target(
			rrap_pk3 ALL
			DEPENDS "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}"
		)

		install(
			FILES "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}"
			DESTINATION "${RRAP_PK3_INSTALL_DIR}/data"
		)
	endif()
endif()

#
# Now generate the entire .apworld
#

set(RRAP_APWORLD_SOURCE_PATH "${CMAKE_SOURCE_DIR}/apworld")
set(RRAP_APWORLD_EXPORT_PATH "${CMAKE_BINARY_DIR}/bin")
set(RRAP_APWORLD_EXPORT_FILE "${RRAP_APWORLD_EXPORT_PATH}/ringracers.apworld")
set(RRAP_APWORLD_STAGING_PATH "${CMAKE_BINARY_DIR}/apworld/ap_staging")

if(RRAP_BUILD_APWORLD)
	if(NOT ZIP_EXECUTABLE)
		message(WARNING "zip was not found; ringracers.apworld cannot be created")
		add_custom_target(
			rrap_apworld ALL
			COMMENT "zip was not found; ringracers.apworld cannot be created"
		)
	else()
		git_latest_tag(RRAP_TAG)
		configure_file(
			"${RRAP_APWORLD_SOURCE_PATH}/version.py.in"
			"${CMAKE_BINARY_DIR}/apworld/version.py"
			@ONLY
		)

		parse_apignore(
			ROOT "${RRAP_APWORLD_SOURCE_PATH}"
			OUT_LIST APWORLD_FILE_LIST
		)

		add_custom_command(
			COMMENT "Staging ringracers.apworld"
			DEPENDS ${APWORLD_FILE_LIST}
			WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
			OUTPUT "${RRAP_APWORLD_STAGING_PATH}/.prepped"

			COMMAND ${CMAKE_COMMAND} -E remove_directory "${RRAP_APWORLD_STAGING_PATH}"
			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_APWORLD_STAGING_PATH}/ringracers"
			COMMAND ${CMAKE_COMMAND} -E touch "${RRAP_APWORLD_STAGING_PATH}/.prepped"
		)

		set(FILE_COMMANDS "")
		foreach(f IN LISTS APWORLD_FILE_LIST)
			set(SOURCE_FILE "${RRAP_APWORLD_SOURCE_PATH}/${f}")
			set(DEST_FILE "${RRAP_APWORLD_STAGING_PATH}/ringracers/${f}")

			get_filename_component(DEST_DIR "${DEST_FILE}" DIRECTORY)
			list(
				APPEND FILE_COMMANDS
				COMMAND ${CMAKE_COMMAND} -E make_directory "${DEST_DIR}"
			)
			list(
				APPEND FILE_COMMANDS
				COMMAND ${CMAKE_COMMAND} -E copy "${SOURCE_FILE}" "${DEST_FILE}"
			)
		endforeach()

		list(
			APPEND FILE_COMMANDS
			COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_BINARY_DIR}/apworld/version.py" "${RRAP_APWORLD_STAGING_PATH}/ringracers/version.py"
		)

		add_custom_command(
			COMMENT "Packaging ringracers.apworld"
			DEPENDS "${RRAP_APWORLD_STAGING_PATH}/.prepped"
			WORKING_DIRECTORY "${RRAP_APWORLD_STAGING_PATH}"
			OUTPUT "${RRAP_APWORLD_EXPORT_FILE}"

			${FILE_COMMANDS}
			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_APWORLD_EXPORT_PATH}"
			COMMAND zip -r "${RRAP_APWORLD_EXPORT_FILE}" ringracers
		)

		add_custom_target(
			rrap_apworld ALL
			DEPENDS "${RRAP_APWORLD_EXPORT_FILE}"
		)
	endif()
endif()
