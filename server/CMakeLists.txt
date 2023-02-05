cmake_minimum_required(VERSION 3.15.0)
cmake_policy(SET CMP0016 NEW)

project(rabbitmq_server VERSION 1.0.0 DESCRIPTION "Работа с брокером сообщений, серверная часть")

include_directories(${CMAKE_SOURCE_DIR}/src)

enable_testing()
add_subdirectory(test)
