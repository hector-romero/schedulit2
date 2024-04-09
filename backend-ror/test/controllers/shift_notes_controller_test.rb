require "test_helper"

class ShiftNotesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @shift_note = shift_notes(:one_a)
  end

  test "should get index" do
    get shift_notes_url, as: :json
    assert_response :success
  end

  test "should create shift_note" do
    assert_difference("ShiftNote.count") do
      post shift_notes_url, params: { shift_note: { note: @shift_note.note, shift_id: @shift_note.shift_id, timestamp: @shift_note.timestamp } }, as: :json
    end

    assert_response :created
  end

  test "should show shift_note" do
    get shift_note_url(@shift_note), as: :json
    assert_response :success
  end

  test "should update shift_note" do
    patch shift_note_url(@shift_note), params: { shift_note: { note: @shift_note.note, shift_id: @shift_note.shift_id, timestamp: @shift_note.timestamp } }, as: :json
    assert_response :success
  end

  test "should destroy shift_note" do
    assert_difference("ShiftNote.count", -1) do
      delete shift_note_url(@shift_note), as: :json
    end

    assert_response :no_content
  end
end
