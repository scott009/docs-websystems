# InquiryCircle - Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    CIRCLES ||--o{ CIRCLE_MEMBERS : has
    CIRCLES ||--o{ MEETINGS : hosts
    USERS ||--o{ CIRCLE_MEMBERS : belongs_to
    USERS ||--o{ MEETING_PARTICIPANTS : participates_in
    USERS ||--o{ MESSAGES : writes
    ROLES ||--o{ CIRCLE_MEMBERS : assigned_to
    MEETINGS ||--o{ MEETING_PARTICIPANTS : has
    
    CIRCLES {
        int id PK
        string name
        text description
        timestamp created_at
        timestamp updated_at
    }
    
    USERS {
        int id PK
        string username
        string email
        string password_hash
        timestamp created_at
    }
    
    ROLES {
        int id PK
        string name
        json permissions
    }
    
    CIRCLE_MEMBERS {
        int id PK
        int circle_id FK
        int user_id FK
        int role_id FK
        timestamp joined_at
    }
    
    MEETINGS {
        int id PK
        int circle_id FK
        string title
        text description
        timestamp scheduled_time
        int duration_minutes
        string jitsi_room_id
        enum status
        int created_by FK
        timestamp created_at
    }
    
    MEETING_PARTICIPANTS {
        int id PK
        int meeting_id FK
        int user_id FK
        timestamp joined_at
        timestamp left_at
        enum status
    }
    
    MESSAGES {
        int id PK
        int circle_id FK
        int user_id FK
        text content
        timestamp created_at
    }
```

## Legend
- **PK**: Primary Key
- **FK**: Foreign Key
- **||--o{**: One-to-Many relationship
- **string**: Variable-length character data
- **text**: Long text data
- **int**: Integer number
- **timestamp**: Date and time
- **enum**: Enumerated type
- **json**: JSON data type for flexible data storage

## Relationship Details
1. **Circles to Circle Members**: One-to-Many (A circle can have many members)
2. **Users to Circle Members**: One-to-Many (A user can be a member of many circles)
3. **Circles to Meetings**: One-to-Many (A circle can have many meetings)
4. **Meetings to Meeting Participants**: One-to-Many (A meeting can have many participants)
5. **Users to Messages**: One-to-Many (A user can write many messages)
6. **Circles to Messages**: One-to-Many (A circle can have many messages)
7. **Roles to Circle Members**: One-to-Many (A role can be assigned to many circle members)

## Notes
- All tables include standard timestamps for creation/updates where appropriate
- Enums are used for status fields to ensure data integrity
- JSON fields are used where flexible data storage is beneficial
- Indexes should be created on all foreign keys for performance optimization
