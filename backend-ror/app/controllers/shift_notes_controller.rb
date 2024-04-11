class ShiftNotesController < ApiController
  before_action :set_shift_note, only: %i[ show update destroy ]

  # GET /shift_notes
  def index
    @shift_notes = ShiftNote.where(shift_id: params['shift_id'])
    render json: @shift_notes
  end

  # GET /shift_notes/1
  def show
    render json: @shift_note
  end

  # POST /shift_notes
  def create
    @shift_note = ShiftNote.create!(shift_note_params)
    render json: @shift_note, status: :created, location: @shift_note
  end

  # PATCH/PUT /shift_notes/1
  def update
    @shift_note.update!(params.permit(:note))
    render json: @shift_note
  end

  # DELETE /shift_notes/1
  def destroy
    @shift_note.destroy!
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_shift_note
      @shift_note = ShiftNote.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def shift_note_params
      params.require([:note, :shift_id])
      params.permit(:note, :shift_id)
    end
end
