#version 460 core

uniform sampler2D tex;
uniform vec4 texOffsetScale;
uniform vec4 colorFilter;

in vec2 texCoord;
in float vDistance;

out vec4 fragColor;

float fogMaxDist = 64.0;
float fogMinDist = 56.0;
vec4  fogColor = vec4(0.0);

void main() {
  float fogFactor = (fogMaxDist - vDistance) / (fogMaxDist - fogMinDist);
  fogFactor = clamp(fogFactor, 0.0, 1.0);
  fragColor = texture(tex, texCoord / texOffsetScale.zw + texOffsetScale.xy);
  fragColor = fragColor * colorFilter;
  fragColor = mix(fogColor, fragColor, fogFactor);
}