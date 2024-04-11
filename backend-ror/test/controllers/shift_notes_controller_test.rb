require "test_helper"

class ShiftNotesControllerTest < ActionDispatch::IntegrationTest
  include AuthenticatedTest

  setup do
    @shift_note = shift_notes(:one_a)
    setup_authentication
  end

  test "should get index" do
    get shift_shift_notes_url(@shift_note.shift), as: :json,  headers: headers
    assert_response :success
  end

  test "should create shift_note" do
    assert_difference("ShiftNote.count") do
      post shift_shift_notes_url(@shift_note.shift), params: { note: @shift_note.note }, as: :json, headers: headers
    end

    assert_response :created
  end

  test "should show shift_note" do
    get shift_note_url(@shift_note), as: :json,  headers: headers
    assert_response :success
  end

  test "should update shift_note" do
    patch shift_note_url(@shift_note), params: { note: @shift_note.note }, as: :json, headers: headers
    assert_response :success
  end

  test "should destroy shift_note" do
    assert_difference("ShiftNote.count", -1) do
      delete shift_note_url(@shift_note), as: :json,  headers: headers
    end

    assert_response :no_content
  end
end
