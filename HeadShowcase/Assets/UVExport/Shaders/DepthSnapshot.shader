
Shader"Custom/DepthSnapshot"
{
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            struct appdata_t
            {
                float4 pos : POSITION;
            };

            struct v2f
            {
                float4 pos : POSITION;
                float depth : TEXCOORD0;
            };
            

            v2f vert(appdata_t v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.pos);
                o.depth = o.pos.z;
                return o;
            }
            float4 frag(v2f i) : SV_TARGET
            {
                return float4(i.depth, 0, 0, 1);
            }
            ENDCG
        }
    }
}
