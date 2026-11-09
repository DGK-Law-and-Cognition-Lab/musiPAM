function pam_reference(infile, outfile, pamdir)
% Run the lab's TestMapping_PAMfunc (unchanged) on mapping problems exported by validate.py.
%   infile:  .mat with N1, N2 (P x n x dn node vectors), E1, E2 (P x n x n x de edge vectors), w (P x 1 objweights)
%   outfile: .mat with Ms (P x n x n mapping matrices) and As (P x 6 analogy scores)
%   pamdir:  folder that holds TestMapping_PAMfunc.m ("PAM public")
addpath(pamdir);
S = load(infile);
P = numel(S.w);
n = size(S.N1, 2);
Ms = zeros(P, n, n);
As = zeros(P, 6);
for p = 1:P
    A1 = cell(n, n);
    A2 = cell(n, n);
    for i = 1:n
        for j = 1:n
            if i == j
                A1{i, j} = reshape(S.N1(p, i, :), 1, []);
                A2{i, j} = reshape(S.N2(p, i, :), 1, []);
            else
                A1{i, j} = reshape(S.E1(p, i, j, :), 1, []);
                A2{i, j} = reshape(S.E2(p, i, j, :), 1, []);
            end
        end
    end
    [M, A] = TestMapping_PAMfunc(A1, n, ones(n), {}, A2, n, ones(n), {}, S.w(p));
    Ms(p, :, :) = M;
    As(p, :) = A;
end
save(outfile, 'Ms', 'As');
end
