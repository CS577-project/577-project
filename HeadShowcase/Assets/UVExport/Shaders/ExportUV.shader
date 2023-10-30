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

            struct appdata_t
            {
                float4 vertex : POSITION;
                float2 texccoord : TEXCOORD0;
            };

            struct v2f
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
};


            v2f vert(appdata_t v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texccoord;
                return o;
            }

            float4 frag(v2f i) : SV_Target
            {
                // Calculate color based on the vertex position in world space
                return float4(i.uv, 0.0f, 1.0);
                //return float4(1.0, 1.0, 1.0, 1.0);
            }
            ENDCG
        }
    }
}
