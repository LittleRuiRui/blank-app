import streamlit as st

st.set_page_config(page_title="TCM 体质小测", page_icon="🌿", layout="centered")

st.markdown("""
<style>
.block-container{max-width:820px;padding-top:2rem;padding-bottom:4rem}
.hero{padding:28px 30px;border-radius:24px;background:#f4f0e6;margin-bottom:18px}
.hero h1{font-size:2.25rem;margin:0 0 .35rem;color:#273127}
.hero p{margin:0;color:#5d675c;font-size:1.03rem}
.card{padding:20px 22px;border:1px solid #e7e2d7;border-radius:18px;margin:12px 0;background:#fffdf8}
.small{font-size:.88rem;color:#757575}
.result-title{font-size:1.35rem;font-weight:700;margin-bottom:.2rem}
</style>
""", unsafe_allow_html=True)

CONSTITUTIONS = {
    "气虚质": {"tag":"容易累 · 气短 · 恢复慢", "food":"规律三餐，保证蛋白质和主食；传统食养常提山药、莲子、白扁豆。", "life":"避免长期熬夜和过度消耗，运动从低到中等强度逐步增加。", "formula":"四君子汤、参苓白术散等常见于传统健脾益气思路。"},
    "阳虚质": {"tag":"怕冷 · 手脚凉 · 喜温", "food":"以正常、温热、易消化饮食为主，不必刻意大量进补；长期大量冰冷食物可少一些。", "life":"注意保暖和规律活动；如果怕冷非常明显，也应排查贫血、甲状腺等原因。", "formula":"理中丸、金匮肾气丸等属于不同辨证场景，不能仅凭“怕冷”自行选择。"},
    "阴虚质": {"tag":"干 · 热感 · 夜间更明显", "food":"保证水分与正常脂肪摄入，少长期重辣、酒精和极端节食。", "life":"优先睡眠和恢复；持续口干也需考虑药物、血糖、环境等现代医学原因。", "formula":"六味地黄丸等常被大众熟知，但传统辨证并非“上火就吃”。"},
    "痰湿质": {"tag":"重 · 黏 · 困 · 痰多", "food":"减少高糖饮料、过量甜食和高油饮食；传统食养常提薏苡仁、赤小豆、冬瓜、山药。", "life":"规律运动、减少久坐、保证睡眠。所谓“祛湿”不等于无限喝祛湿茶。", "formula":"二陈汤是经典燥湿化痰基础方之一；不同寒热虚实会走向完全不同的加减思路。"},
    "湿热质": {"tag":"油 · 黏 · 闷 · 热", "food":"酒精、重油、过量辛辣和高糖是最值得先减少的变量。", "life":"避免长期熬夜和闷热环境；反复皮疹、尿路或消化症状应按疾病本身评估。", "formula":"传统上常见清利湿热思路，但用药方向差异很大，不建议按体质自行套方。"},
    "血瘀质": {"tag":"暗 · 固定 · 瘀滞感", "food":"以均衡饮食为主，不需要为了“活血”大量摄入某一种食物或药材。", "life":"减少久坐、保持活动。异常出血、持续固定疼痛等不能用体质解释。", "formula":"桃红四物汤、血府逐瘀汤等有明确传统辨证语境，并非保健方。"},
    "气郁质": {"tag":"堵 · 闷 · 叹气 · 情绪牵动身体", "food":"规律进食，压力大时尽量避免暴饮暴食、过量咖啡因和酒精。", "life":"运动、睡眠、社交和压力管理往往比“吃什么药”更值得先处理。", "formula":"逍遥散、四逆散等常被用于讲解传统疏肝理气思路，但两者辨证逻辑并不相同。"},
    "特禀质": {"tag":"容易敏感 · 过敏样反应", "food":"重点是识别真正触发因素，而不是盲目忌口。", "life":"反复鼻炎、哮喘、荨麻疹或食物过敏应接受正规过敏评估。", "formula":"传统调理强调个体差异，不适合通过在线测试直接推荐固定方。"},
    "平和质": {"tag":"整体稳定 · 恢复尚可", "food":"保持均衡、多样、不过量的饮食即可。", "life":"稳定的睡眠、运动、压力管理比追求某一种“养生食材”重要。", "formula":"没有必要为了“调体质”主动服用中药。"},
}

QUESTIONS = [
    ("即使睡眠时间尚可，我仍经常觉得疲倦、没精神。", {"气虚质":2,"痰湿质":1}),
    ("稍微活动一下，我就比别人更容易累或气喘。", {"气虚质":2}),
    ("我比身边的人明显更怕冷。", {"阳虚质":2,"气虚质":0.5}),
    ("我的手脚经常发冷。", {"阳虚质":2}),
    ("我经常口干、咽干，晚上更明显。", {"阴虚质":2}),
    ("我有时会有明显的内热感、潮热感，但并没有发烧。", {"阴虚质":2}),
    ("我经常感觉身体沉重、懒得动。", {"痰湿质":2,"气虚质":1}),
    ("我经常觉得嘴里黏、痰多，或喉咙总有东西。", {"痰湿质":2,"湿热质":0.5}),
    ("吃完甜、油或很丰盛的一餐后，我特别容易困重。", {"痰湿质":2,"气虚质":0.5}),
    ("我的脸或头皮很容易出油。", {"湿热质":2,"痰湿质":0.5}),
    ("我经常觉得口苦、口中异味或黏腻。", {"湿热质":2}),
    ("喝酒、吃重辣或油炸后，我特别容易出现不舒服。", {"湿热质":2}),
    ("我的肤色容易显得暗沉，或比较容易出现瘀青。", {"血瘀质":1.5}),
    ("我有某些位置会反复出现比较固定的不适。", {"血瘀质":2}),
    ("压力大时，我特别容易觉得胸口、喉咙或胃里‘堵着’。", {"气郁质":2}),
    ("我经常不自觉地叹气。", {"气郁质":2}),
    ("我的胃口、腹胀或排便很容易被情绪影响。", {"气郁质":2,"气虚质":0.5}),
    ("我的鼻、眼或皮肤很容易因为环境变化出现敏感反应。", {"特禀质":2}),
    ("换季、灰尘、花粉或特定环境很容易让我不舒服。", {"特禀质":2}),
    ("我的睡眠、精力、食欲和排便总体都比较稳定。", {"平和质":2}),
    ("我通常适应天气、饮食和环境变化比较快。", {"平和质":2}),
    ("饭后我经常明显腹胀或昏沉。", {"痰湿质":1.5,"气虚质":1}),
    ("我经常觉得身体或脸容易浮肿。", {"痰湿质":1.5,"阳虚质":0.5}),
    ("我常常因为想很多、压力或情绪波动而觉得身体不舒服。", {"气郁质":2}),
]

SCALE = {"从不":0, "偶尔":1, "有时":2, "经常":3, "几乎总是":4}

st.markdown('<div class="hero"><h1>🌿 TCM 体质小测</h1><p>把传统中医体质翻译成日常能看懂、能行动的生活方式建议。</p></div>', unsafe_allow_html=True)
st.caption("Beta · 约 3 分钟 · 结果用于健康教育，不用于诊断或自动开方")

with st.expander("这份测试在测什么？"):
    st.write("采用常见的九种体质框架：平和、气虚、阳虚、阴虚、痰湿、湿热、血瘀、气郁、特禀。结果显示的是回答模式与传统描述的相似程度，而不是医学诊断。")

answers=[]
with st.form("quiz"):
    for i,(q,_) in enumerate(QUESTIONS,1):
        st.markdown(f"**{i}. {q}**")
        ans=st.radio("", list(SCALE.keys()), index=0, horizontal=True, key=f"q{i}", label_visibility="collapsed")
        answers.append(ans)
    submitted=st.form_submit_button("查看我的体质倾向", use_container_width=True)

if submitted:
    scores={k:0.0 for k in CONSTITUTIONS}
    max_scores={k:0.0 for k in CONSTITUTIONS}
    for ans,(_,weights) in zip(answers,QUESTIONS):
        val=SCALE[ans]
        for k,w in weights.items():
            scores[k]+=val*w
            max_scores[k]+=4*w
    pct={k:(scores[k]/max_scores[k]*100 if max_scores[k] else 0) for k in scores}
    ranked=sorted(pct.items(), key=lambda x:x[1], reverse=True)
    primary=ranked[0]
    secondary=[x for x in ranked[1:4] if x[1]>=35]

    st.divider()
    st.subheader("你的结果")
    st.markdown(f"### {primary[0]}倾向 · {primary[1]:.0f}%")
    st.write(CONSTITUTIONS[primary[0]]["tag"])
    st.progress(min(primary[1]/100,1.0))

    if secondary:
        st.write("**同时出现的倾向：** " + " · ".join([f"{k} {v:.0f}%" for k,v in secondary]))

    st.markdown("#### 为什么可能会这样")
    if primary[0]=="痰湿质":
        st.write("传统中医常用“脾运不足、湿聚成痰”来解释这组重、黏、困的表现。现代生活里，睡眠不足、久坐、总热量过剩、高糖高油饮食等也可能造成相似感受。")
    elif primary[0]=="气郁质":
        st.write("传统中医会把情绪与身体不适之间的联动放在‘气机不畅’的框架里。现代角度则可同时考虑压力、睡眠、自主神经反应与功能性胃肠症状。")
    else:
        st.write("这个结果表示你的回答与该传统体质描述有较高相似度。体质不是疾病名称，也不能替代对具体症状原因的判断。")

    data=CONSTITUTIONS[primary[0]]
    st.markdown("#### 现在可以先做什么")
    st.markdown(f"**怎么吃**  
{data['food']}")
    st.markdown(f"**怎么生活**  
{data['life']}")

    st.markdown("#### 经典方剂怎么理解")
    st.write(data["formula"])
    st.info("方剂部分只介绍传统辨证思路。中药存在药物相互作用、肝肾毒性、孕期禁忌及个体差异；本测试不会根据分数自动给出剂量或让用户自行加减方。")

    with st.expander("看完整九种体质分数"):
        for k,v in ranked:
            st.write(f"{k}  {v:.0f}%")
            st.progress(min(v/100,1.0))

    st.warning("如果存在持续疼痛、明显体重变化、发热、异常出血、呼吸困难、严重过敏反应，或症状持续影响生活，不应只归因于‘体质’，应接受正规医疗评估。")
