require "test_helper"

class ShiftsControllerTest < ActionDispatch::IntegrationTest
  include AuthenticatedTest

  setup do
    @shift = shifts(:one)
    setup_authentication
  end

  test "should get index" do
    get user_shifts_url(@shift.employee_id), as: :json, headers: headers
    assert_response :success
  end

  test "should create shift" do
    assert_difference("Shift.count") do
      post user_shifts_url(@shift.employee_id), params: { end_time: @shift.end_time, start_time: @shift.start_time}, as: :json, headers: headers
    end

    assert_response :created
  end

  test "should show shift" do
    get shift_url(@shift), as: :json, headers: headers
    assert_response :success
  end

  test "should update shift" do
    patch shift_url(@shift), params: { end_time: @shift.end_time, start_time: @shift.start_time, status: @shift.status }, as: :json, headers: headers
    assert_response :success
  end

  test "should destroy shift" do
    assert_difference("Shift.count", -1) do
      delete shift_url(@shift.employee, @shift), as: :json, headers: headers
    end

    assert_response :no_content
  end
end
