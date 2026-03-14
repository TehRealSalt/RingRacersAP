#
# Real basic .apignore handler.
#
# Does not bother with a lot of gitignore
# features, but I'd just like to not need to
# bring in ARCHIPELAGO ITSELF just to
# automatically make a renamed zip...
#

include(CMakeParseArguments)

function(parse_apignore)
	cmake_parse_arguments(
		ARG
		""
		"ROOT;OUT_LIST"
		""
		${ARGN}
	)

	if(NOT ARG_ROOT)
		message(FATAL_ERROR "parse_apignore: must provide ROOT")
	endif()

	if(NOT ARG_OUT_LIST)
		message(FATAL_ERROR "parse_apignore: must provide OUT_LIST")
	endif()

	set(APIGNORE_FILE_STRING ".apignore")

	file(STRINGS "${ARG_ROOT}/${APIGNORE_FILE_STRING}" FILE_LINES)

	set(PATTERN_LIST "")
	foreach(line IN LISTS FILE_LINES)
		string(STRIP "${line}" line)

		if(line STREQUAL "" OR line MATCHES "^#")
			continue()
		endif()

		list(APPEND PATTERN_LIST "${line}")
	endforeach()

	# force .apignore to be in the list
	list(APPEND PATTERN_LIST "${APIGNORE_FILE_STRING}")

	file(
		GLOB_RECURSE ALL_FILES
		RELATIVE "${ARG_ROOT}"
		"${ARG_ROOT}/*"
	)

	function(_should_ignore FILE RESULT)
		set(IS_IGNORED FALSE)

		foreach(pattern IN LISTS PATTERN_LIST)
			if(pattern MATCHES "/$")
				# case 1; directories
				string(LENGTH "${pattern}" plen)
				math(EXPR plen "${plen} - 1")
				string(SUBSTRING "${pattern}" 0 ${plen} dir)
				if(FILE MATCHES "^${dir}(/|$)")
					set(IS_IGNORED TRUE)
					break()
				endif()
			elseif(pattern MATCHES "[*?]")
				# case 2; wildcards
				if(FILE MATCHES "${pattern}")
					set(IS_IGNORED TRUE)
					break()
				endif()
			else()
				# case 3; exact file name
				if(FILE STREQUAL "${pattern}")
					set(IS_IGNORED TRUE)
					break()
				endif()
			endif()

		endforeach()

		set(${RESULT} ${IS_IGNORED} PARENT_SCOPE)
	endfunction()

	set(RETURN_FILES "")
	foreach(f IN LISTS ALL_FILES)
		if(IS_DIRECTORY "${ARG_ROOT}/${f}")
			continue()
		endif()

		_should_ignore("${f}" IGNORED)
		if(NOT IGNORED)
			list(APPEND RETURN_FILES "${f}")
		endif()
	endforeach()

	set(${ARG_OUT_LIST} "${RETURN_FILES}" PARENT_SCOPE)
endfunction()
