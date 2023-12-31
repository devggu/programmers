def inspect(int_bin_list: list) -> bool:
    bin_length = len(int_bin_list)
    
    if len(int_bin_list) != 1:
        center = int_bin_list.pop(bin_length//2) #노드를 pop하고, 하위노드 남기기
        if center == "0" and "1" in int_bin_list: #노드가 0이고 하위노드에 1이 있는경우 False 반환
            return False

        children_nodes = [int_bin_list[:bin_length//2], int_bin_list[bin_length//2:]] #자식노드 분리
        
        # 각 노드 검사중 단 하나의 조건 불일치가 있을시 False 반환
        for node in children_nodes:
            if inspect(node) == False:
                return False
            else:
                continue
            
        return True
    
    else:
        return True
    
# 2진트리에서, 노드 합은 2^n-1개 이므로, 2진수에서 자릿수를 2^n-1로 맞추기 위해 선행 0을 추가해줌 
def zero_append(bin_num_arg: list) -> list:
    bin_num = bin_num_arg
    
    n=1
    while len(bin_num) > 2**n-1:
        n += 1 


    while len(bin_num) < 2**n-1:
        bin_num = ["0"] + bin_num
        
    return bin_num
        

def solution(numbers):
    # 정수 -> 바이너리 변환
    bin_list = [bin(number)[2:] for number in numbers]
    for i in range(len(bin_list)):
        bin_list[i] = list(bin_list[i])
        bin_list[i] = zero_append(bin_list[i])
    

    result = []
    
    # inspect 함수 돌리고 반환되는 값 result에 저장
    for bin_num in bin_list:
        if bin_num == ["0"]:
            result.append(0)
            continue
        if inspect(bin_num) == True:
            result.append(1)
        else:
            result.append(0)
            
            
    return result