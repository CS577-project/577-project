// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader"Custom/ExportUV"
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
                UNITY_TRANSFER_DEPTH(o.depth);
                return o;
            }
            float4 frag(v2f i) : SV_TARGET
            {
                UNITY_OUTPUT_DEPTH(i.depth);
            }
            ENDCG
        }
    }
}
