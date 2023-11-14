Shader "Custom/PasteFace" 
{
	Properties
	{
        // Shader properties
		_MainTex ("Base (RGB)", 2D) = "white" {}
	}
	SubShader
    {
		Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            

            struct appdata
            {
                float4 pos : POSITION;
                float4 pos2 : TEXCOORD0;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float4 pos2 : TEXCOORD0;
            };

            /// unwrap the mesh to the clip space by uv
            /// calculate the position of clip space, and save it to posInClip 
            v2f vert (appdata v)
            {
                v2f o;
                // render the mesh normally
                o.pos = UnityObjectToClipPos(v.pos);
                o.pos2 = v.pos;
                return o;
            }

            
            sampler2D _MainTex;
            // transform the lerped pos in clip to uv, and sample from Style Image
            float4 frag (v2f i) : SV_Target
            {
                // posInClip:[-1,1] -> [0,1]
                float4 uv4 = UnityObjectToClipPos(i.pos2);
                float2 uv = uv4.xy / uv4.w;
                // [-1,1]->[0,1]
                uv = (uv + float2(1,1)) * 0.5;
                uv.y = 1 - uv.y;
                float4 col = tex2D( _MainTex, uv);
                //return float4(0, uv.y, 0,1);
                //float x = uv.x / uv.w;      
                //float y = uv.y / uv.w;
                //if(x < -1)
                //{
                //    return float4(1, 0, 0, 1);
                //}
                //else if(x >= -1 && x <= 1 )
                //{
                //    return float4(0, 1, 0, 1);
                //}
                //else
                //{
                //    return float4(0, 0, 1, 0);
                //}
                return col;
                
            }
            ENDCG
        }
    }
}
