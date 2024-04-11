require "test_helper"

class UsersControllerTest < ActionDispatch::IntegrationTest

  include AuthenticatedTest
  setup do
    setup_authentication
  end

  test "should get index" do
    get users_url, as: :json, headers: headers
    assert_response :success
  end

  test "should create user" do
    user = users(:two)
    user.destroy!
    # TODO check that the user was created with the provided info
    assert_difference("User.count") do
      post users_url, params: { email: user.email, employee_id: user.employee_id, name: user.name, password: user.password, role: user.role }, as: :json, headers: headers
    end

    assert_response :created
  end

  test "should show user" do
    get user_url(@user), as: :json, headers: headers
    assert_response :success
  end

  test "should update user" do
    patch user_url(@user), params: { email: @user.email, employee_id: @user.employee_id, name: @user.name, password: @user.password, role: @user.role }, as: :json, headers: headers
    assert_response :success
  end

  test "should destroy user" do
    assert_difference("User.count", -1) do
      delete user_url(@user), as: :json, headers: headers
    end

    assert_response :no_content
  end
end
