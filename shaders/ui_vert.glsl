#version 460 core

uniform mat4 projMat;
uniform mat4 modelMat;

layout (location = 0) in vec3 inVert;
layout (location = 1) in vec2 vTexCoord;

out vec2 texCoord;

void main() {
  gl_Position = projMat * modelMat * vec4(inVert, 1.0);
  texCoord = vTexCoord;
}