#version 330 core

uniform sampler2D tex;

in vec4 vertColor;
in vec2 texCoord;

out vec4 fragColor;

void main() {
  fragColor = texture(tex, texCoord);
}