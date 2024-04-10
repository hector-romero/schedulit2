require "test_helper"
require 'pbkdf2_password_hasher'


class KnoxTokenTest < ActiveSupport::TestCase

  test "should generate token" do
    assert_not_nil KnoxToken.create_token_string
  end

  test "should generate the correct hash_token" do
    # Generated various tokens using the library in python and copied their hash_token here just to make sure the
    # algorithm is implemented in the same way in both places.
    tokens = [
      ['06fd375fdee33207cf6eae906e6e9377666e9d3e17831fde0faca5212fb0386b', 'a53762ee80192f99bacf302e585895b7fc4030cbaba8af4a82120feae1141e07b41f205ecafd21028ea9e05a8b813a59ef434c4502aa4b2f174d74a2b63dab38'],
      ['6247297cf8bcab42b361ee83e3276c8b3dc74ab25916472d52d0bbf77217182e', '00b348b444e0c82047ebd53cc36df822bd0d7832aa6e8af82d8df024a877343807727ef2d9eaa01c26d42d918813a9dc9e3044e4aa652f9a53c9df98663481c5'],
      ['56c38d90aa5c596b98274287880da1476242c5c1e1b4f46c08a808aa5531b954', 'aed5849f7cdfcd18e83e18eed521d3a2d54cc145e873b50bdf02a665372fd637829c35728a09e9e45eb0b2341ec9f65a46b8c4398c1ad544e2f441139db9c6a3'],
    ]

    tokens.each { |token_hash|
      assert_equal(KnoxToken.hash_token(token_hash[0]), token_hash[1])
    }
  end

  test "should return token key" do
    tokens = [
      ['06fd375fdee33207cf6eae906e6e9377666e9d3e17831fde0faca5212fb0386b', '06fd375f'],
      ['6247297cf8bcab42b361ee83e3276c8b3dc74ab25916472d52d0bbf77217182e', '6247297c'],
      ['56c38d90aa5c596b98274287880da1476242c5c1e1b4f46c08a808aa5531b954', '56c38d90'],
    ]
    tokens.each { |token_key|
      assert_equal(KnoxToken.token_key(token_key[0]), token_key[1])
    }
  end

  test "Should compare digest to the token" do
    # Generated various tokens using the library in python and copied their hash_token here just to make sure the
    # algorithm is implemented in the same way in both places.
    tokens = [
      ['06fd375fdee33207cf6eae906e6e9377666e9d3e17831fde0faca5212fb0386b', 'a53762ee80192f99bacf302e585895b7fc4030cbaba8af4a82120feae1141e07b41f205ecafd21028ea9e05a8b813a59ef434c4502aa4b2f174d74a2b63dab38'],
      ['6247297cf8bcab42b361ee83e3276c8b3dc74ab25916472d52d0bbf77217182e', '00b348b444e0c82047ebd53cc36df822bd0d7832aa6e8af82d8df024a877343807727ef2d9eaa01c26d42d918813a9dc9e3044e4aa652f9a53c9df98663481c5'],
      ['56c38d90aa5c596b98274287880da1476242c5c1e1b4f46c08a808aa5531b954', 'aed5849f7cdfcd18e83e18eed521d3a2d54cc145e873b50bdf02a665372fd637829c35728a09e9e45eb0b2341ec9f65a46b8c4398c1ad544e2f441139db9c6a3'],
    ]
    tokens.each { |token_hash|
      assert KnoxToken.compare_digest(token_hash[0], token_hash[1])
    }

  end
end
