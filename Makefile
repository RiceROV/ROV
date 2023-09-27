# Compiler and Compiler Flags
CXX = g++
CXXFLAGS = -Wall -std=c++11

# Targets
TARGET = pid_controller

# Source and Object Files
SRCDIR = src
OBJDIR = obj
BINDIR = bin
SOURCES = $(shell find $(SRCDIR) -name *.cc)
OBJECTS = $(patsubst $(SRCDIR)/%.cc,$(OBJDIR)/%.o,$(SOURCES))

# Rules
all: $(BINDIR)/$(TARGET)

$(BINDIR)/$(TARGET): $(OBJECTS)
	@mkdir -p $(BINDIR)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cc
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@


.PHONY: clean
clean:
	@rm -rf $(OBJDIR) $(BINDIR)
