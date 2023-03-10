#version 460 core

uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;

layout (location = 0) in vec3 inVert;
layout (location = 1) in vec2 vTexCoord;

out vec2 texCoord;
out float vDistance;

void main() {
  mat4 glob_mat = viewMat * modelMat;
  float d = sqrt(pow(glob_mat[0][0], 2) + pow(glob_mat[0][1], 2) + pow(glob_mat[0][2], 2));
  glob_mat[0].xyz = vec3(d, 0.0, 0.0);
  glob_mat[1].xyz = vec3(0.0, d, 0.0);
  glob_mat[2].xyz = vec3(0.0, 0.0, d);
  gl_Position = projMat * glob_mat * vec4(inVert, 1.0);
  vDistance = length(gl_Position.xyz);
  texCoord = vTexCoord;
}