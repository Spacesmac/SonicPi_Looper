live_loop :drum_pad do
  use_real_time
  sample_name = sync "/osc*/drum_pad"
  sample_name.each() do |x|
    sample x
  end
end

live_loop :effects_receiver do
  use_real_time
  code = sync "/osc*/run_code"
  eval code[0]
end



