schema "main" { }

table "goals" {
    schema = schema.main
    column "id" {
        type = uuid
    }
    column "user_id" {
        type = text
    }
    column "goal" {
        type = text
    }
    column "longest_streak_start" {
        type = datetime
    }
    column "longest_streak_end" {
        type = datetime
        null = true
    }
    column "current_streak_start" {
        type = int
    }
    column "created_at" {
        type = datetime
    }
    column "prompt_at" {
        type = datetime
    }
    primary_key {
        columns = [
            column.id
        ]
    }
    index "user_id_idx" {
        columns = [
            column.user_id
        ]
    }
}

table "completions" {
    schema = schema.main
    column "id" {
        type = uuid
    }
    column "completed_at" {
        type = datetime
    }
    column "goal_id" {
        type = uuid
    }
    foreign_key "goal_id" {
        columns = [column.goal_id]
        ref_columns = [table.goals.column.id]
        on_update = NO_ACTION
        on_delete = CASCADE
    }
}
