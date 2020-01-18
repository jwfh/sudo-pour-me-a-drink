cmake_minimum_required(VERSION 2.8.4)

project(Cocktail_Manual NONE)

include(./modules/UseLATEX/UseLATEX.cmake)

set(PDFLATEX_COMPILER lualatex)

add_latex_document(cocktails.tex)
