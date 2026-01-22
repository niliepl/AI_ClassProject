% =============================================
% SCHOLARSHIP ELIGIBILITY SYSTEM
% Prolog AI Backend - FIXED BASIC REQUIREMENTS DETECTION
% =============================================

:- use_module(library(csv)).
:- use_module(library(lists)).

% -------------------------
% DYNAMIC DATABASE
% -------------------------
:- dynamic student/3.
:- dynamic result/4.

% -------------------------
% CSV DATA IMPORT - FIXED COLUMN MAPPING
% -------------------------

import_students_from_csv(Filename) :-
    format('Loading students from ~w...~n', [Filename]),
    retractall(student(_, _, _)),
    (csv_read_file(Filename, Rows, [skip_header(true)]) ->
        process_csv_rows(Rows, 1),
        format('✅ Successfully loaded students from CSV~n', [])
    ;
        format('❌ Error: Could not read CSV file ~w~n', [Filename]),
        fail
    ).

process_csv_rows([], _).
process_csv_rows([Row|Rest], Index) :-
    process_csv_row(Row, Index),
    NextIndex is Index + 1,
    process_csv_rows(Rest, NextIndex).

process_csv_row(Row, StudentID) :-
    Row =.. [row|Columns],
    create_student_id(StudentID, StudentAtom),
    
    % CORRECTED COLUMN MAPPING for your CSV structure:
    extract_column(Columns, 4, Email),              % D: Email
    extract_column(Columns, 7, Citizenship),        % G: Are you a Malaysian citizen?
    extract_column(Columns, 9, MuslimStatus),       % I: Are you a Malaysian Muslim student?
    extract_column(Columns, 12, Disciplinary),      % L: Do you have any disciplinary record?
    extract_column(Columns, 25, CGPA),              % Y: Current CGPA
    extract_column(Columns, 26, CreditHours),       % Z: Credit Hours Completed
    extract_column(Columns, 29, HouseholdIncome),   % AC: Total Household Monthly Income
    extract_column(Columns, 30, Dependents),        % AD: Number of dependents in your household
    extract_column(Columns, 31, Employment),        % AE: Parents/Guardians employment status
    extract_column(Columns, 32, EducationalLoan),   % AF: Do you have an educational loan?
    extract_column(Columns, 33, ActivityLevel),     % AG: How active are you in co-curricular activities?
    extract_column(Columns, 34, Leadership),        % AH: Do you hold any leadership positions?
    extract_column(Columns, 42, HealthChallenges),  % AP: Do you have any physical/health challenges?
    extract_column(Columns, 43, LivingSituation),   % AQ: Living situation
    extract_column(Columns, 44, Consent),           % AR: Do you agree to let your anonymous data be used?
    
    % Debug: Print first students data for verification
    (StudentID = 1 ->
        format('DEBUG First student data:~n', []),
        format('  Citizenship: ~w~n', [Citizenship]),
        format('  Disciplinary: ~w~n', [Disciplinary]),
        format('  Consent: ~w~n', [Consent])
    ;
        true
    ),
    
    % Assert facts
    assert_student_fact(StudentAtom, email, Email),
    assert_student_fact(StudentAtom, citizenship, Citizenship),
    assert_student_fact(StudentAtom, muslim_status, MuslimStatus),
    assert_student_fact(StudentAtom, disciplinary_record, Disciplinary),
    assert_student_fact(StudentAtom, cgpa, CGPA),
    assert_student_fact(StudentAtom, credit_hours, CreditHours),
    assert_student_fact(StudentAtom, household_income, HouseholdIncome),
    assert_student_fact(StudentAtom, dependents, Dependents),
    assert_student_fact(StudentAtom, employment_status, Employment),
    assert_student_fact(StudentAtom, educational_loan, EducationalLoan),
    assert_student_fact(StudentAtom, activity_level, ActivityLevel),
    assert_student_fact(StudentAtom, leadership_positions, Leadership),
    assert_student_fact(StudentAtom, health_challenges, HealthChallenges),
    assert_student_fact(StudentAtom, living_situation, LivingSituation),
    assert_student_fact(StudentAtom, consent, Consent).

extract_column(Columns, Index, Value) :-
    (nth1(Index, Columns, Value) -> true ; Value = 'Unknown').

create_student_id(Index, StudentAtom) :-
    format(atom(StudentAtom), 'student_~w', [Index]).

assert_student_fact(StudentID, Field, Value) :-
    (Value \= 'Unknown', Value \= '' ->
        assertz(student(StudentID, Field, Value))
    ;
        true
    ).

% -------------------------
% CORE ELIGIBILITY ENGINE - FIXED BASIC REQUIREMENTS DETECTION
% -------------------------

determine_eligibility(StudentID, Decision, Confidence, Explanation) :-
    check_basic_requirements(StudentID, BasicResults),
    (BasicResults = [] ->
        % Student passed basic requirements, evaluate further
        evaluate_academic_profile(StudentID, AcademicTier, AcademicScore),
        evaluate_financial_need(StudentID, FinancialTier, FinancialScore),
        evaluate_cocurricular_profile(StudentID, CocurricularTier, CocurricularScore),
        evaluate_special_factors(StudentID, SpecialFlags, SpecialScore),
        calculate_composite_score(AcademicScore, FinancialScore, CocurricularScore, SpecialScore, TotalScore),
        apply_decision_rules(AcademicTier, FinancialTier, CocurricularTier, SpecialFlags, Decision),
        calculate_confidence(TotalScore, Decision, Confidence),
        generate_success_explanation(StudentID, AcademicTier, FinancialTier, CocurricularTier, SpecialFlags, Decision, Explanation)
    ;
        % Student failed basic requirements
        Decision = 'Not Eligible - Basic Requirements',
        Confidence = 0.1,
        generate_basic_failure_explanation(BasicResults, Explanation)
    ).

% FIXED: More robust basic requirements checking
check_basic_requirements(StudentID, FailedRequirements) :-
    findall(Failure, (
        % Check citizenship - FIXED: Handle multiple positive values
        (student(StudentID, citizenship, Citizenship),
         \+ is_positive_value(Citizenship) -> 
            Failure = 'Not Malaysian citizen'),
         
        % Check disciplinary record - FIXED: Should be negative (no record)
        (student(StudentID, disciplinary_record, Disciplinary),
         \+ is_negative_value(Disciplinary) -> 
            Failure = 'Has disciplinary record'),
         
        % Check consent - FIXED: Handle multiple positive values
        (student(StudentID, consent, Consent),
         \+ is_consent_given(Consent) -> 
            Failure = 'No data consent given')
    ), FailedRequirements).

% Helper predicates for value checking
is_positive_value(Value) :-
    member(Value, ['Yes', 'YES', 'Malaysian', 'Yes, I agree']).

is_negative_value(Value) :-
    member(Value, ['No', 'NO']).

is_consent_given(Value) :-
    member(Value, ['Yes, I agree', 'Yes', 'YES']).

% Generate detailed basic failure explanation
generate_basic_failure_explanation([SingleFailure], Explanation) :-
    format(atom(Explanation), 'Failed basic eligibility: ~w', [SingleFailure]).
generate_basic_failure_explanation(FailedList, Explanation) :-
    atomic_list_concat(FailedList, ', ', FailedString),
    format(atom(Explanation), 'Failed basic eligibility: ~w', [FailedString]).

% Generate success explanation
generate_success_explanation(StudentID, AcademicTier, FinancialTier, CocurricularTier, SpecialFlags, Decision, Explanation) :-
    get_academic_details(StudentID, AcademicDetails),
    get_financial_details(StudentID, FinancialDetails),
    get_activity_details(StudentID, ActivityDetails),
    format(atom(Explanation), 
           'Academic: ~w (~w) | Financial: ~w (~w) | Activities: ~w (~w) | Special Factors: ~w', 
           [AcademicTier, AcademicDetails, FinancialTier, FinancialDetails, CocurricularTier, ActivityDetails, SpecialFlags]).

% Helper predicates for detailed explanations
get_academic_details(StudentID, Details) :-
    student(StudentID, cgpa, CGPA),
    student(StudentID, credit_hours, CreditHours),
    format(atom(Details), 'CGPA: ~w, Credits: ~w', [CGPA, CreditHours]).

get_financial_details(StudentID, Details) :-
    student(StudentID, household_income, Income),
    student(StudentID, dependents, Dependents),
    format(atom(Details), 'Income: ~w, Dependents: ~w', [Income, Dependents]).

get_activity_details(StudentID, Details) :-
    student(StudentID, activity_level, Activity),
    student(StudentID, leadership_positions, Leadership),
    format(atom(Details), 'Activity: ~w, Leadership: ~w', [Activity, Leadership]).

% Academic Evaluation
evaluate_academic_profile(StudentID, AcademicTier, TotalScore) :-
    student(StudentID, cgpa, CGPA),
    student(StudentID, credit_hours, CreditHours),
    cgpa_evaluation(CGPA, CGPATier, CGPAScore),
    credit_hours_evaluation(CreditHours, CreditTier, CreditScore),
    combine_academic_tiers(CGPATier, CreditTier, AcademicTier),
    TotalScore is CGPAScore + CreditScore.

% FIXED: More flexible CGPA matching
cgpa_evaluation(CGPA, excellent, 4.0) :- 
    (sub_string(CGPA, _, _, _, '3.50'); sub_string(CGPA, _, _, _, '4.00'); sub_string(CGPA, _, _, _, '3.50 – 4.00')).
cgpa_evaluation(CGPA, good, 3.0) :- 
    (sub_string(CGPA, _, _, _, '3.00'); sub_string(CGPA, _, _, _, '3.49'); sub_string(CGPA, _, _, _, '3.00 – 3.49')).
cgpa_evaluation(CGPA, average, 2.0) :- 
    (sub_string(CGPA, _, _, _, '2.50'); sub_string(CGPA, _, _, _, '2.99'); sub_string(CGPA, _, _, _, '2.50 – 2.99')).
cgpa_evaluation(_, weak, 1.0).

% FIXED: More flexible credit hours matching
credit_hours_evaluation(CreditHours, advanced, 2.0) :- 
    (sub_string(CreditHours, _, _, _, 'Above 90'); sub_string(CreditHours, _, _, _, 'Above90')).
credit_hours_evaluation(CreditHours, intermediate, 1.5) :- 
    (sub_string(CreditHours, _, _, _, '61–90'); sub_string(CreditHours, _, _, _, '61-90')).
credit_hours_evaluation(CreditHours, beginner, 1.0) :- 
    (sub_string(CreditHours, _, _, _, '30–60'); sub_string(CreditHours, _, _, _, '30-60')).
credit_hours_evaluation(_, early, 0.5).

combine_academic_tiers(excellent, _, tier1).
combine_academic_tiers(good, advanced, tier1).
combine_academic_tiers(good, intermediate, tier2).
combine_academic_tiers(good, beginner, tier2).
combine_academic_tiers(good, early, tier3).
combine_academic_tiers(average, _, tier3).
combine_academic_tiers(weak, _, tier4).

% Financial Evaluation
evaluate_financial_need(StudentID, FinancialTier, TotalScore) :-
    student(StudentID, household_income, Income),
    student(StudentID, dependents, Dependents),
    student(StudentID, employment_status, Employment),
    student(StudentID, educational_loan, Loan),
    income_evaluation(Income, IncomeTier, IncomeScore),
    dependents_evaluation(Dependents, DependentsScore),
    employment_evaluation(Employment, EmploymentScore),
    loan_evaluation(Loan, LoanScore),
    TotalScore is IncomeScore + DependentsScore + EmploymentScore + LoanScore,
    determine_financial_tier(TotalScore, FinancialTier).

% FIXED: More flexible income matching
income_evaluation(Income, b40, 4.0) :- 
    (sub_string(Income, _, _, _, 'B40'); sub_string(Income, _, _, _, 'b40')).
income_evaluation(Income, m40, 2.0) :- 
    (sub_string(Income, _, _, _, 'M40'); sub_string(Income, _, _, _, 'm40')).
income_evaluation(_, t20, 0.0).

% FIXED: More flexible dependents matching
dependents_evaluation(Dependents, 3.0) :- 
    (sub_string(Dependents, _, _, _, '7 and above'); sub_string(Dependents, _, _, _, '7+')).
dependents_evaluation(Dependents, 2.0) :- 
    (sub_string(Dependents, _, _, _, '5–6'); sub_string(Dependents, _, _, _, '5-6')).
dependents_evaluation(Dependents, 1.0) :- 
    (sub_string(Dependents, _, _, _, '3–4'); sub_string(Dependents, _, _, _, '3-4')).
dependents_evaluation(_, 0.5).

% FIXED: More flexible employment matching
employment_evaluation(Employment, 3.0) :- 
    (sub_string(Employment, _, _, _, 'None employed'); sub_string(Employment, _, _, _, 'None')).
employment_evaluation(Employment, 2.0) :- 
    (sub_string(Employment, _, _, _, 'One employed'); sub_string(Employment, _, _, _, 'One')).
employment_evaluation(_, 0.5).

% FIXED: More flexible loan matching
loan_evaluation(Loan, 2.0) :- 
    (Loan = 'Yes'; Loan = 'YES').
loan_evaluation(_, 0.0).

determine_financial_tier(Score, urgent) :- Score >= 8.0.
determine_financial_tier(Score, high) :- Score >= 5.0, Score < 8.0.
determine_financial_tier(Score, medium) :- Score >= 3.0, Score < 5.0.
determine_financial_tier(Score, low) :- Score >= 1.0, Score < 3.0.
determine_financial_tier(_, minimal).

% Co-curricular Evaluation
evaluate_cocurricular_profile(StudentID, CocurricularTier, TotalScore) :-
    student(StudentID, activity_level, Activity),
    student(StudentID, leadership_positions, Leadership),
    activity_evaluation(Activity, ActivityScore),
    leadership_evaluation(Leadership, LeadershipScore),
    TotalScore is ActivityScore + LeadershipScore,
    determine_cocurricular_tier(TotalScore, CocurricularTier).

% FIXED: More flexible activity matching
activity_evaluation(Activity, 3.0) :- 
    (sub_string(Activity, _, _, _, 'Highly active'); sub_string(Activity, _, _, _, 'Highly')).
activity_evaluation(Activity, 2.0) :- 
    (sub_string(Activity, _, _, _, 'Very active'); sub_string(Activity, _, _, _, 'Very')).
activity_evaluation(Activity, 1.5) :- 
    (sub_string(Activity, _, _, _, 'Moderately active'); sub_string(Activity, _, _, _, 'Moderately')).
activity_evaluation(Activity, 1.0) :- 
    (sub_string(Activity, _, _, _, 'Slightly active'); sub_string(Activity, _, _, _, 'Slightly')).
activity_evaluation(_, 0.0).

% FIXED: More flexible leadership matching
leadership_evaluation(Leadership, 2.0) :- 
    (Leadership = 'Yes'; Leadership = 'YES').
leadership_evaluation(_, 0.0).

determine_cocurricular_tier(Score, outstanding) :- Score >= 4.5.
determine_cocurricular_tier(Score, strong) :- Score >= 3.0, Score < 4.5.
determine_cocurricular_tier(Score, moderate) :- Score >= 1.5, Score < 3.0.
determine_cocurricular_tier(Score, basic) :- Score >= 1.0, Score < 1.5).
determine_cocurricular_tier(_, poor).

% Special Factors
evaluate_special_factors(StudentID, SpecialFlags, TotalScore) :-
    findall(Flag-Score, special_factor(StudentID, Flag, Score), FlagScores),
    extract_flags(FlagScores, SpecialFlags),
    calculate_special_score(FlagScores, TotalScore).

% FIXED: More flexible health challenges matching
special_factor(StudentID, health_challenge, 3.0) :-
    student(StudentID, health_challenges, Health),
    (Health = 'Yes'; Health = 'YES').

special_factor(StudentID, financial_hardship, 2.0) :-
    student(StudentID, living_situation, 'Off-campus'),
    student(StudentID, household_income, Income),
    (sub_string(Income, _, _, _, 'B40'); sub_string(Income, _, _, _, 'b40')).

extract_flags([], []).
extract_flags([Flag-_|Rest], [Flag|Flags]) :- extract_flags(Rest, Flags).

calculate_special_score([], 0).
calculate_special_score([_-Score|Rest], Total) :-
    calculate_special_score(Rest, RestTotal),
    Total is Score + RestTotal.

% Decision Rules
apply_decision_rules(tier1, urgent, outstanding, _, 'Full Scholarship').
apply_decision_rules(tier1, urgent, strong, _, 'Full Scholarship').
apply_decision_rules(tier1, high, outstanding, _, 'Full Scholarship').
apply_decision_rules(tier1, high, strong, Flags, 'Full Scholarship') :-
    member(health_challenge, Flags).

apply_decision_rules(tier1, medium, strong, _, 'Partial Scholarship').
apply_decision_rules(tier2, high, _, _, 'Partial Scholarship').
apply_decision_rules(tier2, medium, strong, _, 'Partial Scholarship').
apply_decision_rules(tier2, medium, moderate, _, 'Partial Scholarship').

apply_decision_rules(tier3, urgent, _, Flags, 'Priority Candidate') :-
    member(health_challenge, Flags).
apply_decision_rules(tier2, urgent, poor, Flags, 'Priority Candidate') :-
    member(health_challenge, Flags).

apply_decision_rules(tier4, _, _, _, 'Not Eligible').
apply_decision_rules(_, minimal, _, Flags, 'Not Eligible') :-
    \+ member(health_challenge, Flags).
apply_decision_rules(_, _, _, _, 'Not Eligible').

% Confidence Scoring
calculate_composite_score(Academic, Financial, Cocurricular, Special, Total) :-
    Total is Academic + Financial + Cocurricular + Special.

calculate_confidence(TotalScore, Decision, Confidence) :-
    max_possible_score(20),
    BaseConfidence is TotalScore / 20,
    adjust_confidence(Decision, BaseConfidence, Confidence).

max_possible_score(20).

adjust_confidence('Full Scholarship', Base, Confidence) :-
    Confidence is min(1.0, Base * 1.2).
adjust_confidence('Partial Scholarship', Base, Confidence) :-
    Confidence is min(1.0, Base * 1.1).
adjust_confidence('Priority Candidate', Base, Confidence) :-
    Confidence is Base.
adjust_confidence('Not Eligible', _, 0.2).
adjust_confidence('Not Eligible - Basic Requirements', _, 0.1).

% -------------------------
% BATCH PROCESSING
% -------------------------

evaluate_all_students(Results) :-
    findall(StudentID, student(StudentID, _, _), AllStudents),
    list_to_set(AllStudents, UniqueStudents),
    evaluate_student_list(UniqueStudents, Results).

evaluate_student_list([], []).
evaluate_student_list([StudentID|Rest], [result(StudentID, Decision, Confidence, Explanation)|Results]) :-
    (determine_eligibility(StudentID, Decision, Confidence, Explanation) ->
        true
    ;
        Decision = 'Evaluation Error',
        Confidence = 0.0,
        Explanation = 'Error processing student'
    ),
    evaluate_student_list(Rest, Results).

% -------------------------
% EMAIL-BASED LOOKUP
% -------------------------

% Store results for email lookup
store_results :-
    retractall(result(_, _, _, _)),
    evaluate_all_students(Results),
    forall(member(result(StudentID, Decision, Confidence, Explanation), Results),
           assertz(result(StudentID, Decision, Confidence, Explanation))).

% Find result by email
find_result_by_email(Email, StudentID, Decision, Confidence, Explanation) :-
    student(StudentID, email, Email),
    result(StudentID, Decision, Confidence, Explanation).

% Get all results with emails
get_all_results_with_emails(Results) :-
    findall([StudentID, Email, Decision, Confidence, Explanation],
            (student(StudentID, email, Email),
             result(StudentID, Decision, Confidence, Explanation)),
            Results).

% -------------------------
% CSV EXPORT - FIXED ENCODING
% -------------------------

export_results_to_csv(Filename) :-
    open(Filename, write, Stream, [encoding(utf8)]),
    write(Stream, 'StudentID,Email,Decision,Confidence,Explanation'), nl(Stream),
    forall((student(StudentID, email, Email),
            result(StudentID, Decision, Confidence, Explanation)),
           (write(Stream, StudentID), write(Stream, ','),
            write_q(Stream, Email), write(Stream, ','),
            write_q(Stream, Decision), write(Stream, ','),
            write(Stream, Confidence), write(Stream, ','),
            write_q(Stream, Explanation), nl(Stream))),
    close(Stream).

% Helper to write quoted strings for CSV
write_q(Stream, Value) :-
    (contains_special_char(Value) ->
        format(Stream, '"~w"', [Value])
    ;
        write(Stream, Value)
    ).

contains_special_char(Value) :-
    atom(Value),
    (sub_atom(Value, _, _, _, ',')
    ; sub_atom(Value, _, _, _, '"')
    ; sub_atom(Value, _, _, _, '\n')
    ; sub_atom(Value, _, _, _, '\r')
    ).

% -------------------------
% SYSTEM MANAGEMENT
% -------------------------

show_loaded_students :-
    findall(Student, student(Student, _, _), Students),
    list_to_set(Students, UniqueStudents),
    length(UniqueStudents, Count),
    format('Loaded ~w students:~n', [Count]),
    forall(member(Student, UniqueStudents), 
           (format('  ~w~n', [Student]))).

% Main processing function - accepts filename as argument
process_scholarships(Filename) :-
    format('=== UTP SCHOLARSHIP SYSTEM ===~n~n'),
    format('Processing file: ~w~n', [Filename]),
    format('1. Loading students from CSV...~n'),
    (import_students_from_csv(Filename) ->
        format('2. Showing loaded students...~n'),
        show_loaded_students,
        format('3. Evaluating all students...~n'),
        store_results,
        format('4. Exporting results to CSV...~n'),
        export_results_to_csv('scholarship_results.csv'),
        format('~n✅ Processing completed successfully!~n'),
        format('   Results saved to: scholarship_results.csv~n')
    ;
        format('❌ Processing failed - could not load CSV file~n')
    ).

% Student lookup function
student_lookup(Email) :-
    (find_result_by_email(Email, StudentID, Decision, Confidence, Explanation) ->
        format('Student ID: ~w~n', [StudentID]),
        format('Decision: ~w~n', [Decision]),
        format('Confidence: ~2f~n', [Confidence]),
        format('Explanation: ~w~n', [Explanation])
    ;
        format('❌ No results found for email: ~w~n', [Email])
    ).

% Helper predicates
list_to_set([], []).
list_to_set([H|T], [H|T1]) :-
    remove_all(H, T, T2),
    list_to_set(T2, T1).

remove_all(_, [], []).
remove_all(X, [X|T], T1) :- remove_all(X, T, T1).
remove_all(X, [Y|T], [Y|T1]) :- X \= Y, remove_all(X, T, T1).