Shader"Hidden/SynthesizeStyle"
{
    Properties
    {
        _UVMapImage("Texture", 2D) = "black" {}
        _StyleImage("Texture", 2D) = "black" {}
        _MainTex ("Texture", 2D) = "white" {}
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
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            /// 输入的mesh是脑袋的mesh，绘制的是一个全屏的quad
            /// 按照展uv的方式将脑袋mesh变换成个全屏quad，和base纹理对上，这样pixel shader才能针对当前位置填色，
            /// 另外当前顶点位置也要
            /// 按照正常绘制的方式变换，这样才能得到假装按正常位置着色，应该画在屏幕的哪个位置上，从而采样合成图
            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            sampler2D _MainTex;
            sampler2D _UVMapImage;
            sampler2D _StyleImage;
            
            float4 frag (v2f i) : SV_Target
            {
                // 从uv map中获得当前uv坐标，这个坐标是展开纹理后的坐标
                float4 uv_info = tex2D(_UVMapImage, i.uv);
                
                float4 style_color = tex2D(_StyleImage, uv_info.xy);
                return float4(1,1,1,1);
            }
            ENDCG
        }
    }
}
