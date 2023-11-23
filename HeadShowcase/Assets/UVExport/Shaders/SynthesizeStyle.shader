// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader"Custom/SynthesizeStyle"
{
    Properties
    {
        _StyleTex("Style Image", 2D) = "black" {}
        _MainTex ("Main Texture", 2D) = "white" {}
        _DepthTex("Depth Texture", 2D) = "black" {}
        _MaskTex("Mask Image", 2D) = "black" {}
    }
    SubShader
    {
        // No culling or depth
        Cull Off 
        ZWrite Off 
        ZTest Off

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
                float3 posInView : TEXCOORD1;
                float4 posInModel :TEXCOORD2;
            };

            /// unwrap the mesh to the clip space by uv
            /// calculate the position of clip space, and save it to posInClip 
            v2f vert (appdata v)
            {
                v2f o;
                //float4 pos = UnityObjectToClipPos(v.vertex);
                // [0,1] -> [-1,1]
                o.vertex = float4(v.uv * 2 - float2(1,1), 1, 1);
                // flip v coordinate
                o.vertex.y *= -1;
                o.posInModel = v.vertex;
                o.posInView = UnityObjectToViewPos(v.vertex);
                o.uv = v.uv;

                return o;
            }

            sampler2D _StyleTex;
            sampler2D _DepthTex;
            sampler2D _MainTex;
            sampler2D _MaskTex;
            // transform the lerped pos in clip to uv, and sample from Style Image
            float4 frag (v2f i) : SV_Target
            {
                float4 pos_clip = UnityObjectToClipPos(i.posInModel);
                // divide w to get the NDP range:[-1,1]
                float2 uv = pos_clip.xy / pos_clip.w;
                // posInClip:[-1,1] -> [0,1]
                uv = (uv + float2(1, 1)) * 0.5;
                // flip v
                uv.y = 1 - uv.y;
                // depth test
                float depth = -i.posInView.z;
                float saved_depth = tex2D(_DepthTex, uv);
                float4 maintex_col = tex2D(_MainTex, i.uv);
                float mask = tex2D(_MaskTex, uv);
                //return float4(mask, 0, 0, 1);
                if (depth > saved_depth + 0.001f)
                {
                    return maintex_col;
                }
                else
                {
                    // if it is the edge, then the sampler sample it bilerp, we use the mask as the alpha
                    float4 col = tex2D(_StyleTex, uv);
                    float modified_mask = pow(mask, 3);
                    if(modified_mask < 0.1)
                    {
                        modified_mask = 0;
                    }
                    col = lerp(maintex_col, col, modified_mask);
                    col.a = maintex_col.a;
                    return col;
                }
}           
            ENDCG
        }
    }
}
