require "test_helper"

class AuthTokenTest < ActiveSupport::TestCase
  setup do
    @user = users(:one)
  end

  test "should create token for user with the proper token details" do
    token = AuthToken.create(user: @user)
    assert_not_empty token.digest
    assert_not_empty token.token_key
    assert_not_nil token.token
    assert_equal KnoxToken.token_key(token.token), token.token_key
    assert_equal KnoxToken.hash_token(token.token), token.digest

    token = AuthToken.find(token.digest)
    assert_nil token.token
  end

  test "should have full token available only after creation" do
    token = AuthToken.create(user: @user)
    assert_not_nil token.token

    token = AuthToken.find(token.digest)
    assert_nil token.token
  end
end
