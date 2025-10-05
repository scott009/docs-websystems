# airtimeAllocationSystems


## time share rules 
we've talked about reactions  now I want to talk about another kind of behaviour 
all this pertains to the management of speaking time. 

Jitsi has a dominant speaker 

There could be algorithms to determine the how much speaking time people get 

meeting can be set for a 
start time
end time 
edd time - start time = duration 

adhoc meetings have no calcuable duration until the meeting is done. 
these behavours are enforced by muting 

## Airtime Allocation Rule sets
- Facilitator Override: Key holder can re-allocate time, pause all, or bypass rules.  
- Any rule set could have this property 
  
### Enforcement Mechanism
* Non-enforcement (soft guidance, stats only)
* Enforcement by Muting (system auto-mutes/unmutes per rule).
* Hybrid (warnings, dashboards, then muting if persistent).  

### Ruleset Types
#### non enforcement 
#### Time Lending
 - Participant A donates unused or current time to Participant B.
 - Could be capped (e.g., can’t lend >50% of own allocation).

#### Equal Share 
 - each participant's speaking time = meeting length/#participants 
 
#### Reaction-Based Share reaction based time sharing
   - if you get many positive reactions  your speaking time can be increased
   - if you get many negative reations your time can be reduced 
   - Tunable parameters: weight of each reaction, decay rate (recent reactions matter more)

#### Non-Enforcement / Advisory
- System only reports usage:
-“Alice has used 120% of expected share.”
-“Bob has spoken 10 minutes less than his share.”
 Leaves decision to group/facilitator.

#### Progressive Stack (used in activist circles):
     People who’ve spoken less get higher priority in queue.

#### Round-Robin:
System cycles turns; each gets equal initial slot.

#### Token Economy:
 - Everyone starts with N “tokens” (e.g., 3).   
 - some people could start with more tokens than others - an invited speaker meeting 
  Tokens determine speaking time (e.g 1 token = 30 seconds of speaking time
  tokens might be added and sutracted based on reactions
Maybe reactions cost you a different amounts of tokens  
 
issuing a love costs 2 tokens   
gettin a love gains your 2 tokens 
a like is 1 token as is a dislike, a hate is 2 tomes 

a dislike takes 1 speaking token from the target
a hate takes 2 speaking token2 from target   

##### Token Economy implementations of various rulesets  
Consider implements different models with tokens


### Core Concepts
#### Meeting Parameters
Start Time
End Time
Duration = End – Start
Ad-hoc Meeting: duration is only known retrospectively (measured, not set).
Current Dominant speaker

#### Conceptual Layers
Policy Layer: Define rule (equal, reaction-weighted, token, lending).
Broadcaster Layer: Send warnings, mute commands, UI indicators.
Repository Layer: Store history: durations, reactions, transfers.


#### Dimensions of Time-Sharing
##### Fairness Model
Equal Share: everybody starts with the same entitlement.
Merit-based: more time if others value what you’re saying (via reactions).
Need-based: more time if you’ve spoken less, or if your voice is typically marginalized.
Gift Economy: participants can give time away.
  
##### Level of Enforcement
Advisory: system just shows stats (who’s spoken, how long).
Soft: gentle prompts (“You’ve had a lot of airtime”).
Hard: system controls the mic (mute/unmute).





=======
