# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 0) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "auth_group", id: :integer, default: nil, force: :cascade do |t|
    t.string "name", limit: 150, null: false
    t.index ["name"], name: "auth_group_name_a6ea08ec_like", opclass: :varchar_pattern_ops
    t.unique_constraint ["name"], name: "auth_group_name_key"
  end

  create_table "auth_group_permissions", id: :bigint, default: nil, force: :cascade do |t|
    t.integer "group_id", null: false
    t.integer "permission_id", null: false
    t.index ["group_id"], name: "auth_group_permissions_group_id_b120cbf9"
    t.index ["permission_id"], name: "auth_group_permissions_permission_id_84c5c92e"
    t.unique_constraint ["group_id", "permission_id"], name: "auth_group_permissions_group_id_permission_id_0cd325b0_uniq"
  end

  create_table "auth_permission", id: :integer, default: nil, force: :cascade do |t|
    t.string "name", limit: 255, null: false
    t.integer "content_type_id", null: false
    t.string "codename", limit: 100, null: false
    t.index ["content_type_id"], name: "auth_permission_content_type_id_2f476e4b"
    t.unique_constraint ["content_type_id", "codename"], name: "auth_permission_content_type_id_codename_01ab375a_uniq"
  end

  create_table "authentication_user", id: :bigint, default: nil, force: :cascade do |t|
    t.string "password", limit: 128, null: false
    t.timestamptz "last_login"
    t.boolean "is_superuser", null: false
    t.string "email", limit: 254, null: false
    t.boolean "is_staff", null: false
    t.boolean "is_active", null: false
    t.timestamptz "date_joined", null: false
    t.string "employee_id", limit: 50, null: false
    t.string "name", limit: 150, null: false
    t.string "role", limit: 9, null: false
    t.index "lower((email)::text)", name: "unique_email", unique: true
    t.index ["email"], name: "authentication_user_email_2220eff5_like", opclass: :varchar_pattern_ops
    t.index ["employee_id"], name: "unique_employee_id", unique: true, where: "((employee_id)::text > ''::text)"
  end

  create_table "authentication_user_groups", id: :bigint, default: nil, force: :cascade do |t|
    t.bigint "user_id", null: false
    t.integer "group_id", null: false
    t.index ["group_id"], name: "authentication_user_groups_group_id_6b5c44b7"
    t.index ["user_id"], name: "authentication_user_groups_user_id_30868577"
    t.unique_constraint ["user_id", "group_id"], name: "authentication_user_groups_user_id_group_id_8af031ac_uniq"
  end

  create_table "authentication_user_user_permissions", id: :bigint, default: nil, force: :cascade do |t|
    t.bigint "user_id", null: false
    t.integer "permission_id", null: false
    t.index ["permission_id"], name: "authentication_user_user_permissions_permission_id_ea6be19a"
    t.index ["user_id"], name: "authentication_user_user_permissions_user_id_736ebf7e"
    t.unique_constraint ["user_id", "permission_id"], name: "authentication_user_user_user_id_permission_id_ec51b09f_uniq"
  end

  create_table "django_admin_log", id: :integer, default: nil, force: :cascade do |t|
    t.timestamptz "action_time", null: false
    t.text "object_id"
    t.string "object_repr", limit: 200, null: false
    t.integer "action_flag", limit: 2, null: false
    t.text "change_message", null: false
    t.integer "content_type_id"
    t.bigint "user_id", null: false
    t.index ["content_type_id"], name: "django_admin_log_content_type_id_c4bce8eb"
    t.index ["user_id"], name: "django_admin_log_user_id_c564eba6"
    t.check_constraint "action_flag >= 0", name: "django_admin_log_action_flag_check"
  end

  create_table "django_content_type", id: :integer, default: nil, force: :cascade do |t|
    t.string "app_label", limit: 100, null: false
    t.string "model", limit: 100, null: false

    t.unique_constraint ["app_label", "model"], name: "django_content_type_app_label_model_76bd3d3b_uniq"
  end

  create_table "django_migrations", id: :bigint, default: nil, force: :cascade do |t|
    t.string "app", limit: 255, null: false
    t.string "name", limit: 255, null: false
    t.timestamptz "applied", null: false
  end

  create_table "django_session", primary_key: "session_key", id: { type: :string, limit: 40 }, force: :cascade do |t|
    t.text "session_data", null: false
    t.timestamptz "expire_date", null: false
    t.index ["expire_date"], name: "django_session_expire_date_a5c62663"
    t.index ["session_key"], name: "django_session_session_key_c0390e0f_like", opclass: :varchar_pattern_ops
  end

  create_table "knox_authtoken", primary_key: "digest", id: { type: :string, limit: 128 }, force: :cascade do |t|
    t.timestamptz "created", null: false
    t.bigint "user_id", null: false
    t.timestamptz "expiry"
    t.string "token_key", limit: 8, null: false
    t.index ["digest"], name: "knox_authtoken_digest_188c7e77_like", opclass: :varchar_pattern_ops
    t.index ["token_key"], name: "knox_authtoken_token_key_8f4f7d47"
    t.index ["token_key"], name: "knox_authtoken_token_key_8f4f7d47_like", opclass: :varchar_pattern_ops
    t.index ["user_id"], name: "knox_authtoken_user_id_e5a5d899"
  end

  create_table "shift_shift", id: :bigint, default: nil, force: :cascade do |t|
    t.timestamptz "timestamp", null: false
    t.timestamptz "start_time", null: false
    t.timestamptz "end_time", null: false
    t.string "status", limit: 9, null: false
    t.bigint "employee_id", null: false
    t.index ["employee_id"], name: "shift_shift_employee_id_cb5061a7"
  end

  create_table "shift_shiftnote", id: :bigint, default: nil, force: :cascade do |t|
    t.timestamptz "timestamp", null: false
    t.string "note", limit: 50, null: false
    t.bigint "shift_id", null: false
    t.index ["shift_id"], name: "shift_shiftnote_shift_id_c6e51401"
  end

  add_foreign_key "auth_group_permissions", "auth_group", column: "group_id", name: "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id", deferrable: :deferred
  add_foreign_key "auth_group_permissions", "auth_permission", column: "permission_id", name: "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm", deferrable: :deferred
  add_foreign_key "auth_permission", "django_content_type", column: "content_type_id", name: "auth_permission_content_type_id_2f476e4b_fk_django_co", deferrable: :deferred
  add_foreign_key "authentication_user_groups", "auth_group", column: "group_id", name: "authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id", deferrable: :deferred
  add_foreign_key "authentication_user_groups", "authentication_user", column: "user_id", name: "authentication_user__user_id_30868577_fk_authentic", deferrable: :deferred
  add_foreign_key "authentication_user_user_permissions", "auth_permission", column: "permission_id", name: "authentication_user__permission_id_ea6be19a_fk_auth_perm", deferrable: :deferred
  add_foreign_key "authentication_user_user_permissions", "authentication_user", column: "user_id", name: "authentication_user__user_id_736ebf7e_fk_authentic", deferrable: :deferred
  add_foreign_key "django_admin_log", "authentication_user", column: "user_id", name: "django_admin_log_user_id_c564eba6_fk_authentication_user_id", deferrable: :deferred
  add_foreign_key "django_admin_log", "django_content_type", column: "content_type_id", name: "django_admin_log_content_type_id_c4bce8eb_fk_django_co", deferrable: :deferred
  add_foreign_key "knox_authtoken", "authentication_user", column: "user_id", name: "knox_authtoken_user_id_e5a5d899_fk_authentication_user_id", deferrable: :deferred
  add_foreign_key "shift_shift", "authentication_user", column: "employee_id", name: "shift_shift_employee_id_cb5061a7_fk_authentication_user_id", deferrable: :deferred
  add_foreign_key "shift_shiftnote", "shift_shift", column: "shift_id", name: "shift_shiftnote_shift_id_c6e51401_fk_shift_shift_id", deferrable: :deferred
end
