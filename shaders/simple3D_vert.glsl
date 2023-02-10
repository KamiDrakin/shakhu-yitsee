#version 460 core

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

layout (location = 0) in vec3 inVert;
layout (location = 1) in vec2 vTexCoord;

out vec2 texCoord;
out float vDistance;

void main() {
  gl_Position = projMat * viewMat * modelMat * vec4(inVert, 1.0);
  vDistance = length(gl_Position.xyz);
  texCoord = vTexCoord;
}