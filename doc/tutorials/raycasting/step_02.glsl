void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 normalizedCoord = fragCoord/iResolution.xy;
    vec4 inColor = texture(iChannel0, normalizedCoord);
    if (inColor.a > 0.0)
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    else
        fragColor = vec4(0.0, 0.0, 1.0, 1.0);
}