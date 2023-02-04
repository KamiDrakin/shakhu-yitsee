#version 330 core

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

layout (location = 0) in vec3 inVert;
layout (location = 1) in vec2 vTexCoord;

out vec4 vertColor;
out vec2 texCoord;

void main() {
  gl_Position = projMat * viewMat * modelMat * vec4(inVert, 1.0);
  vertColor = vec4(1.0, 0.0, 1.0, 1.0);
  texCoord = vTexCoord;
}