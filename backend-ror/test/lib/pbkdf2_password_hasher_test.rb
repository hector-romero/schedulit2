require "test_helper"
require 'pbkdf2_password_hasher'



class PasswordTest < ActiveSupport::TestCase
  setup do
    @encoded_password = 'pbkdf2_sha256$720000$pJ0xyf84tAX1zThho4qew0$UQ8ITLb+IvELhDMeV+ctBHZm9B7uriyh1fftTlyjS2E='
    @algorithm = 'pbkdf2_sha256'
    @iterations = 720000
    @salt = 'pJ0xyf84tAX1zThho4qew0'
    @hash = 'UQ8ITLb+IvELhDMeV+ctBHZm9B7uriyh1fftTlyjS2E='

    @password_object = Password.new(@algorithm, @iterations, @salt, @hash)
    @password_decoded = Password.decode(@encoded_password)
  end

  test "should create password with correct params" do
    assert_equal(@password_object.algorithm, @algorithm)
    assert_equal(@password_object.iterations, @iterations)
    assert_equal(@password_object.salt, @salt)
    assert_equal(@password_object.hash, @hash)
  end

  test "should encode password into the correct format" do
    assert_equal(@password_object.to_s, @encoded_password)
  end

  test "should decode password into the correct format" do
    assert_equal(@password_decoded.algorithm, @algorithm)
    assert_equal(@password_decoded.iterations, @iterations)
    assert_equal(@password_decoded.salt, @salt)
    assert_equal(@password_decoded.hash, @hash)

  end
end

class PasswordHasherTest < ActiveSupport::TestCase
  setup do
    @encoded_password = 'pbkdf2_sha256$720000$pJ0xyf84tAX1zThho4qew0$UQ8ITLb+IvELhDMeV+ctBHZm9B7uriyh1fftTlyjS2E='
    @iterations = 720000
    @salt = 'pJ0xyf84tAX1zThho4qew0'
    @hash = 'UQ8ITLb+IvELhDMeV+ctBHZm9B7uriyh1fftTlyjS2E='
    @password = 'password'
  end

  test "should generate password" do
    hash = Pbkdf2PasswordHasher.encode(@password, @salt, @iterations)
    assert_equal(hash, @encoded_password)
  end

  test "should verify password" do
    assert Pbkdf2PasswordHasher.verify(@password, @encoded_password)
    assert Pbkdf2PasswordHasher.verify("testing", Pbkdf2PasswordHasher.encode('testing'))
    assert_not(Pbkdf2PasswordHasher.verify("wrongpassword", @encoded_password))
  end
end
