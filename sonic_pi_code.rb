live_loop :drum_pad do
    use_real_time
    sample_name = sync "/osc*/drum_pad"
    case sample_name[0]
    when 'bd_haus'
      sample :bd_haus
    when 'sn_dub'
      sample :sn_dub
    when 'elec_hi_snare'
      sample :elec_hi_snare
    when 'drum_cymbal_closed'
      sample :drum_cymbal_closed
    end
  end