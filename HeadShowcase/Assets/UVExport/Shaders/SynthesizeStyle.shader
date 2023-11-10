Shader"Custom/SynthesizeStyle"
{
    Properties
    {
        _UVMapImage("Texture", 2D) = "black" {}
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
            };

            /// �����mesh���Դ���mesh�����Ƶ���һ��ȫ����quad
            /// ����չuv�ķ�ʽ���Դ�mesh�任�ɸ�ȫ��quad����base������ϣ�����pixel shader������Ե�ǰλ����ɫ��
            /// ���⵱ǰ����λ��ҲҪ
            /// �����������Ƶķ�ʽ�任���������ܵõ���װ������λ����ɫ��Ӧ�û�����Ļ���ĸ�λ���ϣ��Ӷ������ϳ�ͼ
            /// unwrap the mesh to the clip space
            /// 
            v2f vert (appdata v)
            {
                v2f o;
                // unwrap UV to clip space
                float4 pos = UnityObjectToClipPos(v.vertex);
                o.vertex = float4(v.uv * 2 - float2(1,1), 1, 1);
                o.vertex.y *= -1;
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);     
                
                return o;
            }

            sampler2D _MainTex;
            sampler2D _UVMapImage;
            sampler2D _StyleImage;
            sampler2D _DepthImage;
            
            float4 frag (v2f i) : SV_Target
            {
                // ��uv map�л�õ�ǰuv���꣬���������չ������������
                //float4 uv_info = tex2D(_UVMapImage, i.uv);
                
                
                //float4 style_color = tex2D(_StyleImage, uv_info.xy);
                return float4(i.uv, 0.0f, 1.0f);
            }
            ENDCG
        }
    }
}
