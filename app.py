import streamlit as st
import pandas as pd

# 职业兴趣测试题库（简易版）
interest_test = [
    {"question": "你更喜欢:A.修理机械 B.设计海报 C.分析数据", "type": ["R","A","I"]},
    {"question": "空闲时间你常:A.组织活动 B.研究哲学 C.做手工", "type": ["E","I","R"]}
]

# 加载专业数据
majors = pd.read_csv("majors.csv")

def calculate_holland(answers):
    scores = {"R":0, "I":0, "A":0, "S":0, "E":0, "C":0}
    for i, ans in enumerate(answers):
        scores[interest_test[i]["type"][ord(ans.upper())-65]] += 1
    return max(scores, key=scores.get)

def main():
    st.title("AI高考志愿助手")
    
    # 第一步：输入基本信息
    score = st.slider("你的高考分数", 400, 750, 600)
    city = st.selectbox("意向城市", ["北京","上海","其他"])
    
    # 第二步：兴趣测试
    st.subheader("职业兴趣测试")
    answers = []
    for q in interest_test:
        ans = st.radio(q["question"], ["A","B","C"])
        answers.append(q["type"][ord(ans.upper())-65])
    
    # 第三步：生成推荐
    if st.button("生成推荐"):
        interest = calculate_holland(answers)
        filtered = majors[
            (majors["城市"] == city) & 
            (majors["分数段"].apply(lambda x: eval(f"{score}{x.replace('+','>=').replace('-','<=')}")))
        ]
        for _, row in filtered.iterrows():
            st.success(f"推荐专业：{row['专业']}")
            st.write(f"前景评估：{row['前景']} | 适配度：⭐⭐⭐")

if __name__ == "__main__":
    main()
