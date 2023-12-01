Shader "Custom/TextureBlur"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            uniform float4 _MainTex_TexelSize;
            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                fixed4 col00 = tex2D(_MainTex, float2(i.uv.x - _MainTex_TexelSize.x, i.uv.y - _MainTex_TexelSize.y));
                fixed4 col01 = tex2D(_MainTex, float2(i.uv.x, i.uv.y -_MainTex_TexelSize.y));
                fixed4 col02 = tex2D(_MainTex, float2(i.uv.x + _MainTex_TexelSize.x, i.uv.y -_MainTex_TexelSize.y));

                fixed4 col10 = tex2D(_MainTex, float2(i.uv.x - _MainTex_TexelSize.x, i.uv.y));
                fixed4 col11 = tex2D(_MainTex, float2(i.uv.x, i.uv.y));
                fixed4 col12 = tex2D(_MainTex, float2(i.uv.x + _MainTex_TexelSize.x, i.uv.y ));

                fixed4 col20 = tex2D(_MainTex, float2(i.uv.x - _MainTex_TexelSize.x, i.uv.y + _MainTex_TexelSize.y));
                fixed4 col21 = tex2D(_MainTex, float2(i.uv.x, i.uv.y+ _MainTex_TexelSize.y));
                fixed4 col22 = tex2D(_MainTex, float2(i.uv.x + _MainTex_TexelSize.x, i.uv.y + _MainTex_TexelSize.y));
                fixed4 col = (col00 + col01 + col02 + col10 + col11 + col12 + col20 + col21 + col22) / 9.0;
                return col;
            }
            ENDCG
        }
    }
}
