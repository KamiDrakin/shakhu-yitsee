#version 460 core

uniform sampler2D tex;
uniform vec4 texOffsetScale;
uniform vec4 colorFilter;

in vec2 texCoord;

out vec4 fragColor;

vec4 colorKey = vec4(1, 0, 1, 1);

void main() {
  fragColor = texture(tex, texCoord / texOffsetScale.zw + texOffsetScale.xy);
  if (fragColor == colorKey) discard;
  fragColor = fragColor * colorFilter;
}