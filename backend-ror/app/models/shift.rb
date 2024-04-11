class Shift < ApplicationRecord
  belongs_to :employee, class_name: 'User'
  enum :status, {created: 'created', accepted: 'accepted', completed: 'completed', rejected: 'rejected'},
       default: :created

  validates :end_time, comparison: { greater_than: :start_time }

  self.table_name = 'shift_shift'

  class << self
    private

    def timestamp_attributes_for_create
      super << 'timestamp'  # Todo Rename field to created_at in the django app
    end
  end

end
