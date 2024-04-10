class User < ApplicationRecord
  attribute :is_superuser, :boolean, default: false
  attribute :is_staff, :boolean, default: false
  attribute :is_active, :boolean, default: true
  attribute :employee_id, :string, default: ''
  attribute :name, :string, default: ''
  # https://edgeapi.rubyonrails.org/classes/ActiveRecord/Enum.html
  enum :role, {scheduler: 'scheduler', employee: 'employee'}, default: :scheduler

  self.table_name = 'authentication_user'

  def password
    self[:password]
  end

  def is_scheduler
    self[:role] == :scheduler
  end

  def is_employee
    self[:role] == :employee
  end

  def password=(raw_password)
    self[:password] = Pbkdf2PasswordHasher.encode(raw_password)
  end

  def check_password(raw_password)
    """
        Return a boolean of whether the raw_password was correct
    """
    Pbkdf2PasswordHasher.verify(raw_password, self[:password])
  end

  def as_json(options = nil)
    # This is probably better handled by a serializer, but this is simpler
    # https://github.com/rails-api/active_model_serializers?
    super(only: [:id, :email, :name, :employee_id, :last_login], methods: [:is_scheduler, :is_employee])
  end

  class << self
    private

    def timestamp_attributes_for_create
      super << 'date_joined'
    end
  end

end
