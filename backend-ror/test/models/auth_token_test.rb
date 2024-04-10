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

  test "should return find and validate correct auth token" do
    auth_token = AuthToken.create(user: @user)

    found_auth_token = AuthToken.get_by_token(auth_token.token)
    assert_equal found_auth_token, auth_token
  end

  test "should fail to find and validate auth token if using incorrect key" do
    auth_token = AuthToken.create(user: @user)
    # should fail while using a non valid token
    assert_nil AuthToken.get_by_token("giberish")
    assert_nil AuthToken.get_by_token(1233)

    # Should fail when the token is partially modified
    assert_nil AuthToken.get_by_token(auth_token.token + "strign")
    assert_nil AuthToken.get_by_token(auth_token.token[0..15])

    # Should fail when using the token key
    assert_nil AuthToken.get_by_token(auth_token.token_key)

    # Should fail when using the token digest
    assert_nil AuthToken.get_by_token(auth_token.digest)
    end


end
