# irk-event-worker
message queue worker

# features

### realtime request
- request with location name
- get realtime intel screenshot

### map subscribe
- register specific location name and time
- get scheduled intel screenshot

# specification

### message body

- event_id : message queue uuid
- agent_name : Agent Name in Ingress
- location_name : Keyword of Location (ex. Seoul Station, Central Park, Sydney, Disney Land)
- client_type : Type of Client (ex. Slack, Telegram, Email, etc...)

#### data sample
```json
{
  "event_id": "a573443f-d5c4-4533-a2ac-060af7e0e4bf",
  "agent_name": "SinerDJ",
  "location_name": "Seoul Station",
  "client_type": "slack | telegram | kakaotalk | line | email"
}
```