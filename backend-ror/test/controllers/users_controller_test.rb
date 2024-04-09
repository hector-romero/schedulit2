require "test_helper"

class UsersControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:one)
  end

  test "should get index" do
    get users_url, as: :json
    assert_response :success
  end

  test "should create user" do
    User.delete_all
    assert_difference("User.count") do
      post users_url, params: { user: { date_joined: @user.date_joined, email: @user.email, employee_id: @user.employee_id, is_active: @user.is_active, is_staff: @user.is_staff, is_superuser: @user.is_superuser, last_login: @user.last_login, name: @user.name, password: @user.password, role: @user.role } }, as: :json
    end

    assert_response :created
  end

  test "should show user" do
    get user_url(@user), as: :json
    assert_response :success
  end

  test "should update user" do
    patch user_url(@user), params: { user: { date_joined: @user.date_joined, email: @user.email, employee_id: @user.employee_id, is_active: @user.is_active, is_staff: @user.is_staff, is_superuser: @user.is_superuser, last_login: @user.last_login, name: @user.name, password: @user.password, role: @user.role } }, as: :json
    assert_response :success
  end

  test "should destroy user" do
    assert_difference("User.count", -1) do
      delete user_url(@user), as: :json
    end

    assert_response :no_content
  end
end
