# Makefile for LVGL VPet Demo
# Requires MinGW-w64 and SDL2 development libraries

PROJECT = LVGL_vpet_Demo
CC = gcc
CXX = g++

# Directories
SRCDIR = .
LVGLDIR = lvgl
BUILDDIR = build
BINDIR = bin

# Compiler flags
CFLAGS = -Wall -Wextra -O2 -DLV_CONF_INCLUDE_SIMPLE
CXXFLAGS = $(CFLAGS) -std=c++11
INCLUDES = -I$(SRCDIR) -I$(LVGLDIR)

# Linker flags
LDFLAGS = -lmingw32 -lSDL2main -lSDL2 -lSDL2_mixer -lgdi32 -luser32 -lwinmm

# Source files
SOURCES = main.cpp lvgl_demo.cpp

# Object files
OBJECTS = $(SOURCES:%.cpp=$(BUILDDIR)/%.o)

# Default target
all: setup $(BINDIR)/$(PROJECT).exe

# Setup build directories
setup:
	@if not exist "$(BUILDDIR)" mkdir "$(BUILDDIR)"
	@if not exist "$(BINDIR)" mkdir "$(BINDIR)"

# Build executable
$(BINDIR)/$(PROJECT).exe: $(OBJECTS)
	@echo Linking $(PROJECT)...
	@$(CXX) $(OBJECTS) -o $@ $(LDFLAGS)
	@echo Build completed: $@

# Compile C++ source files
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	@echo Compiling $<...
	@$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Check if LVGL exists
check-lvgl:
	@if not exist "$(LVGLDIR)" (echo ERROR: LVGL directory not found! Please download LVGL PC simulator. && exit 1)

# Clean build files
clean:
	@if exist "$(BUILDDIR)" rmdir /s /q "$(BUILDDIR)"
	@if exist "$(BINDIR)" rmdir /s /q "$(BINDIR)"
	@echo Clean completed.

# Run the demo
run: $(BINDIR)/$(PROJECT).exe
	@echo Running $(PROJECT)...
	@$(BINDIR)/$(PROJECT).exe

# Convert sprites
sprites:
	@echo Converting sprites...
	@python convert_sprites.py

# Show help
help:
	@echo Available targets:
	@echo   all       - Build the project (default)
	@echo   clean     - Clean build files
	@echo   run       - Build and run the project
	@echo   sprites   - Convert PNG sprites to C arrays
	@echo   help      - Show this help
	@echo.
	@echo Requirements:
	@echo   - MinGW-w64 compiler
	@echo   - SDL2 development libraries
	@echo   - LVGL PC simulator in lvgl/ directory

.PHONY: all setup clean run sprites help check-lvgl
