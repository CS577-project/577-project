// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'


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
            };
            

            v2f vert(appdata_t v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.pos);
                return o;
            }
            float frag(v2f i) : SV_TARGET
            {
                float depth = i.pos.w / 10.0f;
                return Linear01Depth(depth);
            }
            ENDCG
        }
    }
}
