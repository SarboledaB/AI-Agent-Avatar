<<<<<<< HEAD
% = = = = = = SUBJECTS = = = = = = %
subject_time(ia,3)
subject_time(pmds,6)
subject_time(projects management,3)

slept_before_class(ia,true)
slept_before_class(ia,true)
slept_before_class(ia,false)
slept_before_class(ia,true)
slept_before_class(ia,false)
slept_before_class(ia,true)
=======
:- dynamic(week/2).
:- dynamic(homework/2).

% = = = = = = SUBJECTS = = = = = = %
subject(ai_introduction).
subject(modern_sw_development_processes).
subject(projects_management).
subject(ux_design).

subject_time(ai_introduction,3).
subject_time(modern_sw_development_processes,6).
subject_time(projects_management,3).
subject_time(ux_design,3).

week(one,106).
week(two,106).
week(three,97).
week(four,97).
week(five,97).
week(six,97).
week(seven,97).

food(salad,10).
food(mango,8).
food(peanutButter,5).
food(beans,7).
food(fish,8).
food(hamburger,-2).
food(pizza,-5).
food(fries,-10).
food(soda,-10).
food(chips,-7).


% = = = = = = RULES = = = = = = %

% = = = = = = 
% Rule 1: A class were understood if you went to class and slept before %
% If you went but didn't sleep, you understood just the half %
% Else you didn't understand it
%
understood_class(S,X):-
    go_to_class(S,true,true), X is 1.
understood_class(S,X):-
    go_to_class(S,true,false), X is 1/2.
understood_class(S,X):-
    go_to_class(S,false,Y), X is 0.

add_homework(Name,Week,Time,AvailableTime):-
    week(Week,Y),
    assertz(homework(Name,Week,Time)),
    AvailableTime is Y-Time,
    retract(week(Week,Y)),
    assertz(week(Week,AvailableTime)).

complete_homework(Name,Time,AvailableTime):-
    homework(Name,Week,X),
    week(Week,Y),
    AvailableTime is Y+X-Time,
    retract(homework(Name,Week,X)),
    retract(week(Week,Y)),
    assertz(week(Week,AvailableTime)).

weekly_health(Week,Score):-
    ate(Food,Week),
    food(Food,Score).

% = = = = = = FACTS = = = = = = %

% = = = = = =
% FIRST WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ai_introduction,true,true).

% = = = = = = 
% SECOND WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ai_introduction,true,true).

% = = = = = = 
% THIRD WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ux_design,true,true).
go_to_class(ai_introduction,true,true).
go_to_class(modern_sw_development_processes,true,true).
go_to_class(modern_sw_development_processes,true,true).

% = = = = = = 
% FOURTH WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ux_design,true,true).
go_to_class(ai_introduction,true,true).
go_to_class(modern_sw_development_processes,true,false).
go_to_class(modern_sw_development_processes,false,true).

% = = = = = = 
% FIFTH WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ux_design,true,false).
go_to_class(ai_introduction,true,false).
go_to_class(modern_sw_development_processes,true,true).
go_to_class(modern_sw_development_processes,true,true).

% = = = = = = 
% SIXTH WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ux_design,true,true).
go_to_class(ai_introduction,true,false).
go_to_class(modern_sw_development_processes,true,true).
go_to_class(modern_sw_development_processes,true,true).

% = = = = = = 
% SENVENTH WEEK %
%
go_to_class(projects_management,true,true).
go_to_class(ux_design,true,true).
go_to_class(ai_introduction,true,true).
go_to_class(modern_sw_development_processes,false,false).
go_to_class(modern_sw_development_processes,true,true).


ate(mango,one).
ate(salad,one).
ate(fish,one).
ate(beans,one).
ate(hamburger,one).
ate(fries,one).
ate(soda,one).
ate(salad,two).
ate(beans,two).
ate(beans,two).
ate(fries,two).
ate(chips,two).
ate(fries,two).
ate(peanutButter,two).
ate(mango,three).
ate(salad,three).
ate(beans,three).
ate(peanutButter,four).
ate(fish,four).
ate(pizza,four).
ate(soda,four).
ate(fries,five).
ate(salad,five).
ate(beans,five).
ate(mango,five).
ate(soda,five).
ate(pizza,six).
ate(soda,six).
ate(peanutButter,seven).
ate(fries,seven).
ate(hamburger,seven).
ate(mango,seven).
>>>>>>> 227197ab5e0f2620064ce31f868c1c6c51dc58ce
