include(APIgnore)

option(RRAP_BUILD_ARCHIPELAGO_PK3 "Create archipelago.pk3" ON)
option(RRAP_BUILD_APWORLD "Create ringracers.apworld" ON)

find_program(ZIP_EXECUTABLE zip)

#
# Generate the game's archipelago.pk3
# It's just our data folder packed into a zip
#

set(RRAP_ARCHIPELAGO_DATA_SOURCE_PATH "${CMAKE_SOURCE_DIR}/apworld/data")
set(RRAP_ARCHIPELAGO_DATA_EXPORT_PATH "${CMAKE_BINARY_DIR}/bin/data")
set(RRAP_ARCHIPELAGO_DATA_EXPORT_FILE "${RRAP_ARCHIPELAGO_DATA_EXPORT_PATH}/archipelago.pk3")
set(RRAP_ARCHIPELAGO_DATA_STAGING_PATH "${CMAKE_BINARY_DIR}/apworld/staging")

if(RRAP_BUILD_ARCHIPELAGO_PK3)
	if(NOT ZIP_EXECUTABLE)
		add_custom_target(
			rrap_pk3 ALL
			COMMENT "zip was not found; archipelago.pk3 cannot be created"
		)
	else()
		add_custom_command(
			COMMENT "Staging archipelago.pk3"
			DEPENDS "${RRAP_ARCHIPELAGO_DATA_SOURCE_PATH}"
			WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
			OUTPUT "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/.prepped"

			COMMAND ${CMAKE_COMMAND} -E remove_directory "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}"
			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/archipelago"
			COMMAND ${CMAKE_COMMAND} -E copy_directory "${RRAP_ARCHIPELAGO_DATA_SOURCE_PATH}" "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/archipelago"
		)

		add_custom_command(
			COMMENT "Packaging archipelago.pk3"
			DEPENDS "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}/.prepped"
			WORKING_DIRECTORY "${RRAP_ARCHIPELAGO_DATA_STAGING_PATH}"
			OUTPUT "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}"

			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_ARCHIPELAGO_DATA_EXPORT_PATH}"
			COMMAND zip -r "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}" archipelago
		)

		add_custom_target(
			rrap_pk3 ALL
			DEPENDS "${RRAP_ARCHIPELAGO_DATA_EXPORT_FILE}"
		)
	endif()
endif()

#
# Now generate the entire .apworld
#

set(RRAP_APWORLD_SOURCE_PATH "${CMAKE_SOURCE_DIR}/apworld")
set(RRAP_APWORLD_EXPORT_PATH "${CMAKE_BINARY_DIR}/bin")
set(RRAP_APWORLD_EXPORT_FILE "${RRAP_APWORLD_EXPORT_PATH}/ringracers.apworld")

if(RRAP_BUILD_APWORLD)
	if(NOT ZIP_EXECUTABLE)
		add_custom_target(
			rrap_apworld ALL
			COMMENT "zip was not found; ringracers.apworld cannot be created"
		)
	else()
		parse_apignore(
			ROOT "${RRAP_APWORLD_SOURCE_PATH}"
    		OUT_LIST APWORLD_FILE_LIST
		)

		add_custom_command(
			COMMENT "Packaging ringracers.apworld"
			DEPENDS ${APWORLD_FILE_LIST}
			WORKING_DIRECTORY "${RRAP_APWORLD_SOURCE_PATH}"
			OUTPUT "${RRAP_APWORLD_EXPORT_FILE}"

			COMMAND ${CMAKE_COMMAND} -E make_directory "${RRAP_APWORLD_EXPORT_PATH}"
			COMMAND zip "${RRAP_APWORLD_EXPORT_FILE}" ${APWORLD_FILE_LIST}
		)

		add_custom_target(
			rrap_apworld ALL
			DEPENDS "${RRAP_APWORLD_EXPORT_FILE}"
		)
	endif()
endif()
