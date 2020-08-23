# irk-event-worker
message queue worker


# 기능

### 실시간 요청
- 메신저 or 웹 -> 메시지큐 -> 크롤러

### 구독형
- 메신저 or 웹 -> 메시지큐 -> 매니저 -> DB -> 매니저 -> 메시지큐 -> 크롤러