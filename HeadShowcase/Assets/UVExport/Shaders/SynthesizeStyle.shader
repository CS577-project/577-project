Shader"Custom/SynthesizeStyle"
{
    Properties
    {
        _StyleImage("Texture", 2D) = "black" {}
        _MainTex ("Texture", 2D) = "white" {}
        _DepthTex("Texture", 2D) = "black" {}
    }
    SubShader
    {
        // No culling or depth
        Cull Off ZWrite Off ZTest Always

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
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
                float4 posInClip : TEXCOORD1;
            };

            /// unwrap the mesh to the clip space by uv
            /// calculate the position of clip space, and save it to posInClip 
            v2f vert (appdata v)
            {
                v2f o;
                // unwrap UV to clip space
                float4 pos = UnityObjectToClipPos(v.vertex);
                o.vertex = float4(v.uv * 2 - float2(1,1), 1, 1);
                o.vertex.y *= -1;
                o.uv = v.uv;
                o.posInClip = pos;
                return o;
            }

            sampler2D _StyleImage;
            sampler2D _DepthImage;
            // transform the lerped pos in clip to uv, and sample from Style Image
            float4 frag (v2f i) : SV_Target
            {
                // posInClip:[-1,1] -> [0,1]
                float2 uv = i.posInClip + float2(1, 1) * 0.5;
                uv.y *= -1;
                float4 col = tex2D(_StyleImage, uv);
                return col;
            }
            ENDCG
        }
    }
}
