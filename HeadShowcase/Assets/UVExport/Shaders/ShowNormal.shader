Shader "Custom/ShowNormal"
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
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
                float3 posInView :TEXCOORD0;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.posInView = UnityObjectToViewPos(v.vertex);
                return o;
            }

            float4 frag (v2f i) : SV_Target
            {
                // sample the texture
                float3 posInView = i.posInView;
                posInView.z = -posInView.z;
                float val = dot(normalize(posInView), (0,0,1));
                //float val = dot(normalize(i.normal), (0,0,-1));
                //val = -val;
                return float4(val,0,0,1);
            }
            ENDCG
        }
    }
}
