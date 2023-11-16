
add_executable(
    2015
    main.cpp
    src/day1.cpp
    src/day2.cpp
    src/day3.cpp
    src/day4.cpp
    src/day5.cpp
    src/day7.cpp
)

target_include_directories(
    2015
    PRIVATE
    include
)

target_compile_options(
    2015
    PRIVATE
    -Wall
    -Werror
    -Wextra
#    -Wconversion
#    -Wsign-conversion
#    -pedantic
#    -pedantic-errors
)

find_package(OpenSSL REQUIRED)
target_link_libraries(2015 PRIVATE OpenSSL::SSL)

file(COPY ../inputs DESTINATION ${CMAKE_BINARY_DIR}/2015)