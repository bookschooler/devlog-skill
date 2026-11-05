# devlog-skill (한국어)

코딩 에이전트와 나눈 대화를 **하루 개발 일지**로 바꿔 주는 [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)이야.
뭘 만들었는지, 뭘 배웠는지, 왜 그렇게 정했는지를 남기고, 꼬리 질문이 어떻게 깨달음과 결정으로
이어졌는지를 "꼬꼬무 맵"으로 쌓아 가.

`SKILL.md` 폴더 형식을 읽고 파일을 읽고 쓸 수 있는 에이전트면 다 쓸 수 있어. 훅이나 외부 서비스는 필요 없어.

## 설치

에이전트의 스킬 폴더에 이 폴더를 복사하면 돼. Claude Code라면:

```powershell
git clone https://github.com/bookschooler/devlog-skill "$HOME\.claude\skills\devlog"   # 저장소를 / 내 스킬 폴더 안 devlog로 복제한다
```

```bash
git clone https://github.com/bookschooler/devlog-skill ~/.claude/skills/devlog
```

다른 에이전트는 그 에이전트가 스킬을 읽는 폴더에 넣어 줘.

## 사용법

작업을 마치고 이렇게 말해:

> 오늘 일지 써줘

처음 쓰면 에이전트가 프로젝트 맨 위 폴더에 `DEVLOG.md`를 만들어. `language: ko`로 두면 일지가 한국어로 써지고,
프로젝트 이름·태그·**기록 금지** 목록(비밀키, 내부 주소, 팀원 이름 등)도 여기서 정해.
한국어 설정 템플릿은 `templates/DEVLOG.ko.md`에 있어.

대시보드는 언제든 이렇게 만들어:

```powershell
python path\to\devlog\scripts\build_dashboard.py .   # 파이썬으로 / 대시보드 스크립트를 / 현재 프로젝트 폴더에 대해 실행한다
```

`devlog/dashboard.html` 한 장이 만들어져. 파이썬 기본 라이브러리만 써서 따로 설치할 게 없어.

## 들어 있는 것

```
SKILL.md / SKILL.ko.md          언제 쓰나 + 작업 순서 (에이전트는 SKILL.md를 읽음)
references/rules(.ko).md        작성 규칙: 결과 vs 공부, 출처 등급 A~D·1~3, 대화에 없던 사실 금지
templates/daily(.ko).md         하루 일지 틀
templates/map.json              꼬꼬무 맵: root → task → question → insight → decision
templates/DEVLOG(.ko).md        사용자별 설정
scripts/build_dashboard.py      일지 + 맵 → dashboard.html
```

## 라이선스

MIT
