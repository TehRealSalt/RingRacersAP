# Update from https://github.com/N00byKing/APCpp
# License: GNU Lesser General Public License v2.1

cmake_minimum_required(VERSION 3.10)

project(APCpp)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

add_library(APCpp STATIC Archipelago.cpp Archipelago.h)
add_library(APCpp::APCpp ALIAS APCpp)

target_include_directories(APCpp PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")

set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(ENABLE_TESTING OFF CACHE BOOL "" FORCE)
set(ENABLE_PROGRAMS OFF CACHE BOOL "" FORCE)

# Enable TLS. On Windows, build mbedTLS
set(USE_TLS ON CACHE BOOL "Enable TLS support" FORCE)
if ((WIN32 AND USE_TLS) OR USE_MBED_TLS)
	set(APCPP_MBEDTLS_VER 3.6.2)
	execute_process(COMMAND ${CMAKE_COMMAND} -E remove -f mbedtls-${APCPP_MBEDTLS_VER})
	execute_process(COMMAND ${CMAKE_COMMAND} -E tar xzf ${CMAKE_CURRENT_SOURCE_DIR}/mbedtls-${APCPP_MBEDTLS_VER}.tar.bz2 ${CMAKE_BINARY_DIR}/mbedtls-${APCPP_MBEDTLS_VER})
	set(USE_STATIC_MBEDTLS_LIBRARY ON CACHE BOOL "" FORCE)
	set(MBEDTLS_INCLUDE_DIRS ${CMAKE_BINARY_DIR}/mbedtls-${APCPP_MBEDTLS_VER}/include)
	set(MBEDTLS_VERSION_GREATER_THAN_3 ${MBEDTLS_INCLUDE_DIRS})
	set(MBEDTLS_LIBRARY mbedtls)
	set(MBEDX509_LIBRARY mbedx509)
	set(MBEDCRYPTO_LIBRARY mbedcrypto)
	add_subdirectory(${CMAKE_BINARY_DIR}/mbedtls-${APCPP_MBEDTLS_VER} mbedtls_bin)
endif ((WIN32 AND USE_TLS) OR USE_MBED_TLS)

set(IXWEBSOCKET_INSTALL OFF CACHE BOOL "" FORCE)
add_subdirectory(IXWebSocket)
include_directories(IXWebSocket)
target_link_libraries(APCpp PRIVATE ixwebsocket)

if (MINGW)
	target_link_libraries(APCpp PRIVATE -static -static-libstdc++ -static-libgcc)
endif(MINGW)

add_subdirectory(jsoncpp)
set_property(TARGET jsoncpp_static PROPERTY POSITION_INDEPENDENT_CODE ON)
include_directories(jsoncpp/include)
target_link_libraries(APCpp PRIVATE jsoncpp_static)

if (WIN32)
	target_link_libraries(APCpp PRIVATE ws2_32)
endif(WIN32)
