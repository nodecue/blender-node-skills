---
title: Utilities Text
section: utilities
description: "Utilities (Text): String formatting, composition, and text-to-geometry utilities."
tags: find, format, match, special, text, utilities
blender_support: "5.0+"
blender_verified: 5.1, 5.2
last_verified: "2026-07-18"
---

## Utilities Text

Reference nodes for `Utilities Text`. Total: **15** nodes.

### Find in String — `FunctionNodeFindInString`
- **Notes:** The Find in String node finds the number of times a substring occurs in a string, and the position of the start of the first match.
- **Inputs:**
  - `String` (`STRING`)
  - `Search` (`STRING`)
- **Outputs:**
  - `First Found` (`INT`)
  - `Count` (`INT`)


### Format String — `FunctionNodeFormatString`
- **Notes:** The Format String node inserts values into a string using either a Python compatible string format syntax or Blender’s format specifier syntax. This node simplifies string construction, allowing values to be combined and formatted without converting numbers to strings or using multiple concatenate nodes.
- **Inputs:**
  - `Format` (`STRING`)
  - `Unnamed` (`CUSTOM`)
- **Outputs:**
  - `String` (`STRING`)
- **Example:** Format: `Count: {}` Inputs: Integer with value 5 Result: `Count: 5` Format: `X: {}, Y: {}` Inputs: Float 1.5, Float 2.0 Result: `X: 1.5, Y: 2.0` Format: `Size: {width} x {height}` Inputs: width=1920, height=1080 Result: `Size: 1920 x 1080` Format: `Frame_{:04}` Inputs: Integer 12 Result: `Frame_0012` Format: `##.00` Input: Float 3.1415 Result: `03.14` Format: `/output/image_{:04}.png` Input: Integer 42 Result: `/output/image_0042.png`.
- **Tip:** Python Syntax references: - Python Format String Syntax - {fmt} Format String Syntax
- **Warning:** Input names must be valid identifiers and must be unique. If a name is invalid, the format operation may fail or produce incorrect output.


### Join Strings — `GeometryNodeStringJoin`
- **Notes:** The Join Strings node combines any number of input strings into the output string. The order of the result depends on the vertical ordering of the inputs in the multi-input socket.
- **Inputs:**
  - `Delimiter` (`STRING`)
  - `Strings` (`STRING`)
- **Outputs:**
  - `String` (`STRING`)
- **Tip:** This node can be used to create a multi-line string for the String to Curves Node, when combined with the line break output from the Special Characters Node.


### Match String — `FunctionNodeMatchString`
- **Notes:** The Match String node compares two string values and outputs a Boolean result based on the selected operation. It is useful for conditional logic involving string comparisons, such as matching object names or attribute values.
- **Inputs:**
  - `String` (`STRING`)
  - `Operation` (`MENU: Starts With, Ends With, Contains`)
  - `Key` (`STRING`)
- **Outputs:**
  - `Result` (`BOOLEAN`)


### Replace String — `FunctionNodeReplaceString`
- **Notes:** The Replace String node replaces a string segment with another. Using the node to add the newline character to a string. 
- **Inputs:**
  - `String` (`STRING`)
  - `Find` (`STRING`)
  - `Replace` (`STRING`)
- **Outputs:**
  - `String` (`STRING`)
- **Example:** Using the node to add the newline character to a string.


### Reverse String — `FunctionNodeReverseString`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Reverse the characters of a string.
- **Inputs:**
  - `String` (`STRING`)
- **Outputs:**
  - `String` (`STRING`)


### Set String Case — `FunctionNodeSetStringCase`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Convert a string's case (mode enum, e.g. upper/lower).
- **Inputs:**
  - `String` (`STRING`)
  - `Case` (`MENU`)
- **Outputs:**
  - `String` (`STRING`)


### Slice String — `FunctionNodeSliceString`
- **Notes:** The Slice String node extracts a string segment from a larger string.
- **Inputs:**
  - `String` (`STRING`)
  - `Position` (`INT`)
  - `Length` (`INT`)
- **Outputs:**
  - `String` (`STRING`)


### Special Characters — `FunctionNodeInputSpecialCharacters`
- **Notes:** The Special Characters node is used to output string characters that can’t be typed directly with the keyboard.
- **Inputs:** None
- **Outputs:**
  - `Line Break` (`STRING`)
  - `Tab` (`STRING`)
- **Tip:** This node can be used to create a multi-line string for the String to Curves Node, when combined with the Join Strings Node or the Replace String Node.


### Split String — `FunctionNodeSplitString`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Split a string by a delimiter into a string list; consume with list nodes.
- **Inputs:**
  - `String` (`STRING`)
  - `Separator` (`STRING`)
- **Outputs:**
  - `List` (`STRING`)


### String Length — `FunctionNodeStringLength`
- **Notes:** The String Length node outputs the number of characters in the input string.
- **Inputs:**
  - `String` (`STRING`)
- **Outputs:**
  - `Length` (`INT`)


### String to Curves — `GeometryNodeStringToCurves`
- **Notes:** The String to Curves node converts a string to curve instances. Each unique character used in the string is converted to a curve once, and further uses of that character are instances of the same geometry. The name of each instance geometry is the character it represents. This makes processing the output geometry very efficient, because each unique character only has to be processed once. However, it means that the result will be the same for every instance of the same character. To process each character individually, the Realize Instances Node can be used.
- **Inputs:**
  - `String` (`STRING`)
  - `Size` (`FLOAT`)
  - `Character Spacing` (`FLOAT`)
  - `Word Spacing` (`FLOAT`)
  - `Line Spacing` (`FLOAT`)
  - `Text Box Width` (`FLOAT`)
  - `Text Box Height` (`FLOAT`)
- **Outputs:**
  - `Curve Instances` (`GEOMETRY`)
  - `Remainder` (`STRING`)
  - `Line` (`INT`)
  - `Pivot Point` (`VECTOR`)
- **Example:** The node can be used to make overflowing text boxes.
- **Tip:** Socket inspection can be used to see the value of the string input used when the node was evaluated, by holding the mouse over the socket.
- **Properties:**
  - `overflow` (OVERFLOW, SCALE_TO_FIT, TRUNCATE) — OVERFLOW: Let the text use more space than the specified height; SCALE_TO_FIT: Scale the text size to fit inside the width and height; TRUNCATE: Only output curves that fit within the width and height. Output the remainder...
  - `align_x` (LEFT, CENTER, RIGHT, JUSTIFY, FLUSH) — LEFT: Align text to the left; CENTER: Align text to the center; RIGHT: Align text to the right
  - `align_y` (TOP, TOP_BASELINE, MIDDLE, BOTTOM_BASELINE, BOTTOM) — TOP: Align text to the top; TOP_BASELINE: Align text to the top line's baseline; MIDDLE: Align text to the middle
  - `pivot_mode` (MIDPOINT, TOP_LEFT, TOP_CENTER, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT)


### String to Value — `FunctionNodeStringToValue`
- **Notes:** The String to Value node converts a text string into a numerical value. This is useful for parsing numbers from text input, file data, or dynamically generated strings. The node reads characters from the beginning of the string until a valid number is parsed. If parsing is unsuccessful, the node outputs a floating-point value of 0.
- **Inputs:**
  - `String` (`STRING`)
- **Outputs:**
  - `Value` (`FLOAT`)
  - `Length` (`INT`)
- **Example:** Converting the string `"3.1415"` with Float selected outputs a value of `3.1415` and a length of `6`.


### Trim String — `FunctionNodeTrimString`
- **Version:** Blender `5.2+`; verified `5.2`.
- **Evidence:** Blender 5.2 Geometry Nodes release notes; Blender 5.2.0 live readback.
- **Notes:** Trim characters from the ends of a string.
- **Inputs:**
  - `String` (`STRING`)
  - `Characters` (`STRING`)
  - `Whitespace` (`BOOLEAN`)
  - `Start` (`BOOLEAN`)
  - `End` (`BOOLEAN`)
- **Outputs:**
  - `String` (`STRING`)


### Value to String — `FunctionNodeValueToString`
- **Notes:** The Value to String node generates string representation of the input value.
- **Inputs:**
  - `Value` (`FLOAT`)
  - `Decimals` (`INT`)
- **Outputs:**
  - `String` (`STRING`)
